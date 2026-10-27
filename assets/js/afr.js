(function () {
  'use strict';

  const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  const subscribers = new Map();
  const queuedJobs = new Map();
  const scrollState = {
    position: window.scrollY || 0,
    velocity: 0,
    speed: 0,
    direction: 0,
    phase: 'idle'
  };
  const runtime = {
    tier: 3,
    samples: 0,
    totalFrameMs: 0,
    slowFrames: 0,
    stableFrames: 0,
    longTasks: 0,
    lastPressureAt: 0,
    lastTransitionAt: 0
  };
  let frameHandle = null;
  let lastFrameTime = 0;
  let elapsedTime = 0;
  let lastDispatchTime = 0;
  let profile = null;
  let stopQueuedJobs = null;
  let lastScrollTime = 0;
  let scrollStopHandle = null;

  const tierModes = ['static', 'lite', 'balanced', 'full'];
  const tierQuality = [0, 0.55, 0.78, 1];
  const tierFps = [0, 30, 45, 60];

  function classifyScroll(speed) {
    if (speed >= 1.2) return 'fast';
    if (speed >= 0.04) return 'slow';
    return 'idle';
  }

  function capabilityTier() {
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    const saveData = connection && connection.saveData === true;
    const lowMemory = typeof navigator.deviceMemory === 'number' && navigator.deviceMemory <= 2;
    const lowCpu = typeof navigator.hardwareConcurrency === 'number' && navigator.hardwareConcurrency <= 2;
    if (saveData || lowMemory || lowCpu) return 1;
    // Touch devices do not expose hover intent and are more sensitive to
    // sustained paint/compositor work. Keep their default motion balanced;
    // the user can still see the full page and explicit interactions remain.
    if (window.matchMedia('(pointer: coarse)').matches) return 2;
    if ((typeof navigator.deviceMemory === 'number' && navigator.deviceMemory <= 4)
      || (typeof navigator.hardwareConcurrency === 'number' && navigator.hardwareConcurrency <= 4)) return 2;
    return 3;
  }

  function hardConstraint() {
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (reducedMotionQuery.matches) return { mode: 'static', reason: 'reduced-motion' };
    if (typeof window.requestAnimationFrame !== 'function' || !('visibilityState' in document)) {
      return { mode: 'static', reason: 'runtime-unsupported' };
    }
    if (connection && connection.saveData === true) return { mode: 'lite', reason: 'save-data' };
    return null;
  }

  function readProfile() {
    const hard = hardConstraint();
    if (hard?.mode === 'static') {
      return {
        mode: 'static', quality: 0, targetFps: 0, reason: hard.reason,
        scrollPhase: scrollState.phase, pressure: 'hard'
      };
    }

    const hintTier = hard?.mode === 'lite' ? 1 : capabilityTier();
    const effectiveTier = Math.min(hintTier, runtime.tier);
    let quality = tierQuality[effectiveTier];
    let targetFps = tierFps[effectiveTier];
    let reason = effectiveTier < 3 ? 'adaptive-budget' : 'default';

    if (runtime.lastPressureAt && window.performance.now() - runtime.lastPressureAt < 2600) {
      reason = 'frame-pressure';
    }
    if (scrollState.phase === 'fast') {
      quality *= 0.65;
      targetFps = Math.min(targetFps, 30);
      reason = 'fast-scroll';
    } else if (scrollState.phase === 'slow') {
      quality *= 0.85;
      targetFps = Math.min(targetFps, 45);
    }

    return {
      mode: tierModes[effectiveTier],
      quality: Math.round(quality * 100) / 100,
      targetFps,
      reason,
      scrollPhase: scrollState.phase,
      pressure: runtime.lastPressureAt ? 'observed' : 'none'
    };
  }

  function isPaused() {
    return document.visibilityState === 'hidden' || profile.mode === 'static';
  }

  function publishProfile() {
    const doc = document.documentElement;
    doc.dataset.afr = profile.mode;
    doc.dataset.afrScroll = profile.scrollPhase;
    doc.dataset.afrQuality = String(profile.quality);
    doc.dataset.afrFps = String(profile.targetFps);
    window.dispatchEvent(new CustomEvent('portfolio:afrprofilechange', {
      detail: { ...profile }
    }));
  }

  function requestFrame() {
    if (frameHandle !== null || isPaused() || subscribers.size === 0) return;
    frameHandle = window.requestAnimationFrame(dispatchFrame);
  }

  function resetFeedbackWindow() {
    runtime.samples = 0;
    runtime.totalFrameMs = 0;
    runtime.slowFrames = 0;
    runtime.longTasks = 0;
  }

  function maybeAdapt(now) {
    if (hardConstraint()?.mode === 'static' || runtime.samples < 24) return;
    const average = runtime.totalFrameMs / runtime.samples;
    const pressured = runtime.slowFrames >= 7 || average >= 24 || runtime.longTasks >= 2;
    const canTransition = now - runtime.lastTransitionAt >= 1400;

    if (pressured && canTransition && runtime.tier > 1) {
      runtime.tier -= 1;
      runtime.stableFrames = 0;
      runtime.lastPressureAt = now;
      runtime.lastTransitionAt = now;
      resetFeedbackWindow();
      refreshProfile();
      return;
    }

    if (!pressured && runtime.longTasks === 0) runtime.stableFrames += runtime.samples;
    if (runtime.stableFrames >= 72 && canTransition && runtime.tier < 3) {
      runtime.tier += 1;
      runtime.stableFrames = 0;
      runtime.lastTransitionAt = now;
      resetFeedbackWindow();
      refreshProfile();
    }
  }

  function noteFrame(delta, now) {
    if (!Number.isFinite(delta) || delta <= 0 || delta > 250) return;
    runtime.samples += 1;
    runtime.totalFrameMs += delta;
    if (delta >= 26) runtime.slowFrames += 1;
    maybeAdapt(now);
  }

  function dispatchFrame(now) {
    frameHandle = null;
    if (isPaused()) return;

    const frameInterval = profile.targetFps > 0 ? 1000 / profile.targetFps : 0;
    if (lastDispatchTime && now - lastDispatchTime < frameInterval - 0.5) {
      requestFrame();
      return;
    }

    const delta = lastFrameTime ? Math.min(100, Math.max(0, now - lastFrameTime)) : 16.67;
    lastFrameTime = now;
    lastDispatchTime = now;
    elapsedTime += delta;
    noteFrame(delta, now);

    const frame = {
      time: now,
      delta,
      elapsed: elapsedTime,
      profile: { ...profile },
      scroll: { ...scrollState }
    };

    subscribers.forEach((callback) => {
      try {
        callback(frame);
      } catch (error) {
        window.setTimeout(() => { throw error; }, 0);
      }
    });

    if (subscribers.size > 0) requestFrame();
  }

  function refreshProfile() {
    const nextProfile = readProfile();
    const changed = !profile || Object.keys(nextProfile).some((key) => nextProfile[key] !== profile[key]);
    profile = nextProfile;
    if (changed) publishProfile();

    if (isPaused() && frameHandle !== null) {
      window.cancelAnimationFrame(frameHandle);
      frameHandle = null;
    }
    requestFrame();
  }

  function stopScroll() {
    scrollStopHandle = null;
    lastScrollTime = 0;
    scrollState.velocity = 0;
    scrollState.speed = 0;
    scrollState.direction = 0;
    scrollState.phase = 'idle';
    refreshProfile();
  }

  function handleScroll() {
    const now = window.performance.now();
    const position = window.scrollY || document.documentElement.scrollTop || 0;
    const deltaTime = lastScrollTime ? Math.max(8, now - lastScrollTime) : 16.67;
    const deltaPosition = position - scrollState.position;
    const velocity = deltaPosition / deltaTime;

    scrollState.position = position;
    scrollState.velocity = velocity * 1000;
    scrollState.speed = Math.abs(velocity * 1000);
    scrollState.direction = Math.sign(deltaPosition);
    const nextPhase = classifyScroll(Math.abs(velocity));
    const phaseChanged = nextPhase !== scrollState.phase;
    scrollState.phase = nextPhase;
    lastScrollTime = now;

    if (scrollStopHandle !== null) window.clearTimeout(scrollStopHandle);
    scrollStopHandle = window.setTimeout(stopScroll, 120);
    // Position/velocity are still sampled on every native scroll event, but
    // profile publication only needs to happen when the scroll phase changes.
    // Re-reading media/capability state for every wheel event adds avoidable
    // main-thread work exactly while the user is trying to scroll.
    if (phaseChanged) refreshProfile();
  }

  function register(id, callback) {
    if (typeof id !== 'string' || !id || typeof callback !== 'function') {
      throw new TypeError('AFR.register(id, callback) requires a string id and function callback');
    }
    subscribers.set(id, callback);
    requestFrame();
    return function unregister() {
      subscribers.delete(id);
      requestFrame();
    };
  }

  function schedule(id, callback) {
    if (typeof id !== 'string' || !id || typeof callback !== 'function') {
      throw new TypeError('AFR.schedule(id, callback) requires a string id and function callback');
    }
    queuedJobs.set(id, callback);
    if (stopQueuedJobs) return;
    stopQueuedJobs = register('__queued-work', (frame) => {
      const jobs = Array.from(queuedJobs.values());
      queuedJobs.clear();
      const stop = stopQueuedJobs;
      stopQueuedJobs = null;
      stop();
      jobs.forEach((job) => job(frame));
    });
  }

  function installStaticPolicy() {
    if (!document.head || document.head.querySelector('[data-afr-policy]')) return;
    const style = document.createElement('style');
    style.dataset.afrPolicy = 'true';
    style.textContent = [
      'html[data-afr="static"] *,html[data-afr="static"] *::before,html[data-afr="static"] *::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}',
      'html[data-afr="static"] [data-afr-loop]{animation:none!important}',
      'html[data-afr="lite"] [data-afr-heavy],html[data-afr="balanced"] [data-afr-heavy]{animation-play-state:paused!important}'
    ].join('');
    document.head.appendChild(style);
  }

  function installHealthUiCleanup() {
    const s = '.live-rail,.oc-live-strip,#__flow_health_strip,[data-live-status],[data-health-detail]';
    document.querySelectorAll(s).forEach((node) => node.remove());
  }

  profile = readProfile();
  installStaticPolicy();
  installHealthUiCleanup();
  publishProfile();

  if ('PerformanceObserver' in window) {
    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        if (!entries.length) return;
        runtime.longTasks += entries.length;
        runtime.stableFrames = 0;
        runtime.lastPressureAt = window.performance.now();
        refreshProfile();
      });
      observer.observe({ type: 'longtask', buffered: true });
    } catch (error) {
    }
  }

  document.addEventListener('visibilitychange', refreshProfile, { passive: true });
  window.addEventListener('scroll', handleScroll, { passive: true });
  reducedMotionQuery.addEventListener?.('change', refreshProfile);
  window.addEventListener('pageshow', refreshProfile, { passive: true });
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  connection?.addEventListener?.('change', refreshProfile);

  window.portfolioAFR = Object.freeze({
    register,
    schedule,
    getProfile: () => ({ ...profile }),
    getScrollState: () => ({ ...scrollState }),
    isActive: () => !isPaused(),
    refresh: refreshProfile
  });
  requestFrame();
})();

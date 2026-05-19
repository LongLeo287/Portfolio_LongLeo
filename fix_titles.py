
import re

replacements = {
    '04 - GAMING GEAR RAZER': 'Banner Gaming Gear Razer',
    '27INCH 2K': 'Poster Màn Hình 27 Inch 2K',
    'ADATA XPG-4K': 'Banner ADATA XPG 4K',
    'ASUS VY279HF-1': 'Banner Màn Hình ASUS VY279HF (B?n 1)',
    'ASUS VY279HF': 'Banner Màn Hình ASUS VY279HF (B?n 2)',
    'Banner LCD 100Hz best seller MSI': 'Banner Màn Hình MSI 100Hz',
    'Banner LCD 100Hz best seller': 'Banner Màn Hình 100Hz',
    'Banner LCD VIEWSONIC': 'Banner Màn Hình ViewSonic',
    'BANNER PC CYBER': 'Banner PC Cyber Gaming',
    'BANNER Ph? NOEL 2025': 'Banner Giáng Sinh 2025 (Ph?)',
    'BANNER T?NG NOEL 2025': 'Banner Giáng Sinh 2025 (Chính)',
    'ComboMain+CPUIntelZ890+COREULTRA': 'Combo Main Z890 & CPU Intel Core Ultra',
    'FRAME NOEL 2025': 'Khung ?nh Giáng Sinh 2025',
    'FRAME NOEL FLASHSALE 2025': 'Khung ?nh Flash Sale Giáng Sinh',
    'GALAX VIVANCE-32Q': 'Banner Màn Hình GALAX Vivance-32Q',
    'HPNY 2025 BANNER PH?': 'Banner Nam M?i 2025 (Ph?)',
    'HPNY 2025 BANNER T?NG': 'Banner Nam M?i 2025 (Chính)',
    'HPNY FRAME HOT DEAL': 'Khung ?nh Nam M?i Hot Deal',
    'HPNY FRAME': 'Khung ?nh Chúc M?ng Nam M?i',
    'Khuy?n Mãi Gaming Gear Lên T?i 70%': 'Banner Khuy?n Mãi Gaming Gear',
    'LCD VAN PHÒNG 2K 100HZ-120HZ': 'Banner Màn Hình Van Phòng 2K',
    'LCD VAN PHÒNG 2K 100HZ-120HZViewSonic': 'Banner Màn Hình Van Phòng ViewSonic',
    'MAG 275QF_2': 'Banner MSI MAG 275QF (B?n 1)',
    'MAG 275QF_Web 2': 'Banner MSI MAG 275QF (B?n 2)',
    'MÀN HÌNH OLED SAMSUNG': 'Banner Màn Hình Samsung OLED',
    'MÀN HÌNH OLED': 'Banner Màn Hình OLED',
    'Màn hình Gaming FullHD 180Hz Viewsonic': 'Banner ViewSonic Gaming 180Hz',
    'Màn hình Gaming FullHD 180Hz': 'Banner Màn Hình Gaming 180Hz',
    'Màn hình Ultrawide': 'Banner Màn Hình Ultrawide',
    'PC Gaming - Màn Hình Chính Hãng sale off lên t?i 50%': 'Banner Khuy?n Mãi PC & Màn Hình',
    'PC TU BUILD 2': 'Banner T? Build PC (B?n 2)',
    'PC TU BUILD': 'Banner T? Build PC (B?n 1)',
    'Philips Innovation Festival banner Web': 'Banner Web Philips Innovation Festival',
    'Razer DeathAdder': 'Banner Chu?t Razer DeathAdder',
    'Razer Viper': 'Banner Chu?t Razer Viper',
    'Viewsonic VA240-H': 'Banner ViewSonic VA240-H',
    'Viewsonic VA240-H_WEB': 'Banner Web ViewSonic VA240-H',
    'vivance 01': 'Banner GALAX Vivance',
    '[27': 'Poster Màn Hình 27 Inch',
    '338309422_877369133359512_706987': 'Banner Qu?ng Cáo S? Ki?n (M?u 1)',
    '340082900_247040477742770_651010': 'Banner Qu?ng Cáo S? Ki?n (M?u 2)',
    'BG BAEMIN 2 21': 'Background BAEMIN',
    '26 - PET GROOMING & HOTEL': 'Poster D?ch V? Pet Grooming',
    'Avatar FB VPET''S 8': '?nh Ð?i Di?n VPET''S (M?u 1)',
    'Avatar FB VPET''S': '?nh Ð?i Di?n VPET''S (M?u 2)',
    'Banner Bravecto Drontal-1': 'Banner S?n Ph?m Thú Y (M?u 1)',
    'Banner Bravecto Drontal-2': 'Banner S?n Ph?m Thú Y (M?u 2)',
    'Banner Bravecto Drontal-3': 'Banner S?n Ph?m Thú Y (M?u 3)',
    'Banner Bravecto Drontal_1': 'Banner S?n Ph?m Thú Y (M?u 4)',
    'BOSS ÐI SPA & KHÁCH S?N - TR?I NGHI?M NHU SEN-2': 'Banner D?ch V? Spa Thú Cung (M?u 1)',
    'BOSS ÐI SPA & KHÁCH S?N - TR?I NGHI?M NHU SEN': 'Banner D?ch V? Spa Thú Cung (M?u 2)',
    'HAPPY DAY-1': 'Poster S? Ki?n Happy Day (M?u 1)',
    'HAPPY DAY-2': 'Poster S? Ki?n Happy Day (M?u 2)',
    'HAPPY DAY-3': 'Poster S? Ki?n Happy Day (M?u 3)',
    'HAPPY DAY': 'Poster S? Ki?n Happy Day (M?u 4)',
    'PET GROOMING & HOTEL': 'Poster D?ch V? Thú Cung',
    'Poster 8': 'Poster Qu?ng Cáo S? Ki?n',
    'VPET''S COVER FB 8': '?nh Bìa Facebook VPET''S',
    'Uu dãi thành viên': 'Banner Uu Ðãi Thành Viên',
    
    # Photography replacements
    '17936426665_9a6a1c2e99_o': '?nh Chân Dung / S? Ki?n (B? 1)',
    '20206526396_bab68b9c0e_o': '?nh Chân Dung / S? Ki?n (B? 2)',
    '20573404096_678f81dba1_o': '?nh Chân Dung / S? Ki?n (B? 3)',
    '20946762359_f56eacc966_o': '?nh Chân Dung / S? Ki?n (B? 4)',
    '21106781196_a9f0d5648c_o': '?nh Chân Dung / S? Ki?n (B? 5)',
    '21133255925_9a6139ff62_o': '?nh Chân Dung / S? Ki?n (B? 6)',
    '24418545264_363c456e5f_o': '?nh Chân Dung / S? Ki?n (B? 7)',
    '24422325963_2afe78034d_o': '?nh Chân Dung / S? Ki?n (B? 8)',
    '24422329913_3c5a7863da_o': '?nh Chân Dung / S? Ki?n (B? 9)',
    '24681632339_4a89284de2_o': '?nh Chân Dung / S? Ki?n (B? 10)',
    '33758877192_02bbbc59c3_o': '?nh Chân Dung / S? Ki?n (B? 11)',
    '358ed537-0319-47ce-9c4b-965ea52c780b-compressed': '?nh S?n Ph?m Ð?c Trung',
    '36152395453_1b9f25c33f_o': '?nh Chân Dung / S? Ki?n (B? 12)',
    '36152398043_d5104f2dbf_o': '?nh Chân Dung / S? Ki?n (B? 13)',
    '36152405003_7792e73b5c_o': '?nh Chân Dung / S? Ki?n (B? 14)',
    '36961097465_6563c0e9c1_o': '?nh Chân Dung / S? Ki?n (B? 15)',
    '36961099185_0c0a60bcab_o': '?nh Chân Dung / S? Ki?n (B? 16)',
    'FB_IMG_1559963917462-compressed': 'Hình ?nh Luu Tr? (Archive)',
    'IMG_0072': '?nh Ngh? Thu?t (B? 1)',
    'IMG_0398': '?nh Ngh? Thu?t (B? 2)',
    'IMG_0754': '?nh Ngh? Thu?t (B? 3)',
    'IMG_1098': '?nh Ngh? Thu?t (B? 4)',
    'IMG_5125_jpg': '?nh Ngh? Thu?t (B? 5)',
    'IMG_5129_jpg': '?nh Ngh? Thu?t (B? 6)',
    'IMG_9944': '?nh Ngh? Thu?t (B? 7)'
}

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def replacer(match):
    prefix = match.group(1)
    title = match.group(2)
    # Remove HTML entities for matching, or just match strictly
    import html
    clean_title = html.unescape(title)
    # The current titles might have missing accents because of terminal output earlier,
    # but let's do a fuzzy match or just a simple replace.
    # Actually, we can just replace any title if it is a substring of the text
    pass

# We will just do a direct string replace for the ones we know
new_text = text
for k, v in replacements.items():
    # Because some strings have unicode encoding issues in the terminal output, 
    # we need to be careful. For example: 'MÀN HÌNH OLED' might be in the file as 'MÀN HÌNH OLED'.
    # We will compile a regex to ignore case and accents if possible, or just standard replace.
    new_text = new_text.replace(f'<h3>{k}</h3>', f'<h3>{v}</h3>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Done.')


# Harnis Registration App

## Set Email & Password
1. Buka aplikasi CMD (commend prompt)
2. setx APP_EMAIL "email@mail.com"
3. setx APP_PASSWORD "password"

## Cara Cari IP Address
1.	Connect laptop ke hotspot handphone yang akan dipakai (pakai internet hp)
2.	Buka aplikasi CMD (commend prompt)
3.	Ketik ipconfig -all | findstr “IPv4”
4.	Akan muncul seperti: IPv4 Address . . . . . . . . 172.20.10.6
5.	Berarti IP address kita adalah 172.20.10.6


## Blast QR CODE
1.	Buka aplikasi CMD (commend prompt)
2.	Ketik cd desktop
3.	Ketik cd harnis_registration_app
4.	Masukan excel attendance list ke folder harnis_registration_app
5.	Ketik python qr_generator.py --ip "172.20.10.2" --subject "This is a test subject" --excel_path "test_attendance_list"

## Run Aplikasi Scanner
1.	Buka aplikasi CMD (commend prompt)
2.	Ketik cd desktop
3.	Ketik cd harnis_registration_app
4.	Ketik flask run --host=0.0.0.0

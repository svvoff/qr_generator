import qrcode

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=2,
    border=1,
)

qr.add_data('''
ST00012|Name=ДЕПАРТАМЕНТ ФИНАНСОВ ГОРОДА МОСКВЫ (ГБОУ Школа имени Маяковского л/с 2607542000900468)|PersonalAcc=40601810245253000002|BankName=ГУ БАНКА РОССИИ ПО ЦФО Г. МОСКВА 35|BIC=044525000|CorrespAcc=0|Sum=250000|Purpose=СНИЛС:ХХХХХХ03307.Оплата за Калинин Никита Васильевич (ЛС 09020),Дог-р №1069-ДО, 2018-19 уч.год Развивающий курс "Математика +" Горская И.Ф., Октябрь.2018, НДС не обл.|PayeeINN=7723103106|DrawerStatus=24|KPP=772301001|CBC=07500000000000000137|OKTMO=45396000|lastName=Калинина|firstName=Светлана|middleName=Васильевна|payerAddress=109044, Москва г, Дубровская 1-я ул, дом № 2а, кв.18|contract=1069-ДО|persAcc=09020|childFio=Калинин Никита Васильевич|uin=0349347501810000000132623
''')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("generated.png")

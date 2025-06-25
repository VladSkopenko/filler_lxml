from fpdf import FPDF
from fpdf.enums import XPos, YPos

class TTHForm(FPDF):
    def __init__(self):
        super().__init__()
        # Добавляем шрифты Times New Roman
        self.add_font("TimesNewRoman", "", "fonts/TIMES.TTF", uni=True)
        self.add_font("TimesNewRoman", "B", "fonts/TIMESBD.TTF", uni=True)
        self.add_font("TimesNewRoman", "I", "fonts/TIMESI.TTF", uni=True)
        self.add_font("TimesNewRoman", "BI", "fonts/TIMESBI.TTF", uni=True)

        self.set_auto_page_break(auto=False)
        self.add_page()
        self.set_font("TimesNewRoman", "", 10)

    def header(self):
        self.set_font("TimesNewRoman", "B", 14)
        self.cell(0, 10, "ТОВАРНО-ТРАНСПОРТНА НАКЛАДНА", ln=True, align="C")

    def create_fields(self):
        self.set_font("TimesNewRoman", "", 10)

        # Пример поля для номера
        self.cell(40, 10, "№", 0, 0)
        self.text_field(name="number", x=25, y=25, w=40, h=8, border=1)
        self.cell(0, 10, "от", 0, 1)

        # Пример поля для автомобиля
        self.cell(40, 10, "Автомобіль", 0, 0)
        self.text_field(name="car", x=45, y=35, w=60, h=8, border=1)
        self.ln(15)

        # Автомобіль
        self.cell(35, 10, "Автомобіль:", align="L")
        self.text_field("car", x=40, y=self.get_y()-1, w=80, h=6)

        self.cell(35, 10, "Причіп/напівпричіп:", align="L")
        self.text_field("trailer", x=115, y=self.get_y()-1, w=80, h=6, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.ln(8)

        # Перевізник
        self.cell(45, 10, "Автомобільний перевізник:", align="L")
        self.text_field("carrier", x=60, y=self.get_y()-1, w=100, h=6, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.ln(8)

        self.cell(20, 10, "ЄДРПОУ:", align="L")
        self.text_field("carrier_edrpou", x=30, y=self.get_y()-1, w=50, h=6)
        self.ln(8)

        # Водій
        self.cell(20, 10, "Водій:", align="L")
        self.text_field("driver", x=30, y=self.get_y()-1, w=80, h=6)
        self.ln(8)

        # Вид перевезень авто
        self.cell(50, 10, "Вид перевезень авто:", align="L")
        self.text_field("transport_type", x=65, y=self.get_y()-1, w=50, h=6)
        self.ln(8)

        # Замовник
        self.cell(40, 10, "Замовник (платник):", align="L")
        self.text_field("customer", x=55, y=self.get_y()-1, w=90, h=6)
        self.ln(8)

        self.cell(20, 10, "ЄДРПОУ:", align="L")
        self.text_field("customer_edrpou", x=30, y=self.get_y()-1, w=40, h=6)

        self.cell(20, 10, "Адреса:", align="L")
        self.text_field("customer_address", x=75, y=self.get_y()-1, w=80, h=6)

pdf = TTHForm()
pdf.create_fields()
pdf.output("ttn_form.pdf")
print("PDF-форма создана!")

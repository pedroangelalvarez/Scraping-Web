import asyncio
from pyppeteer import launch
from datetime import date, timedelta

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://sistemas.minagri.gob.pe/sisap/portal2/mayorista/#')
    await page.waitFor(4000)
    await page.click('#CHK_1105_CHK')
    await page.waitFor(1000)
    yesterday = date.today() - timedelta(days=1)
    yesterday = yesterday.strftime('%d/%m/%Y')
    await page.evaluate('''() => {
         document.getElementById('fecha').value = "'''+yesterday+'''";
    }''')
    print(yesterday)
    await page.waitFor(3000)
    await page.click('#consultar')
    await page.waitFor(3000)
    datos = await page.evaluate('''() => {
         return { tabla : document.getElementById('reporte').outerHTML,}
    }''')
    if (len(str(datos['tabla']))>125):
       data = str(datos['tabla'])
       fecha =""
       precio =""
       fecha = data[data.find('Fecha: ')+7:data.find('Fecha: ')+17]
       precio = data[data.find('</td></tr></tbody>')-4:data.find('</td></tr></tbody>')]
       print(fecha)
       print(precio)
    else:
       print("no datos")
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())

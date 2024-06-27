def sctaskScraper(soup):
    task_form = soup.find(id="sc_task.form_header")
    sctask = task_form.get('data-form-title', '').split("|")[0].strip()
    print(sctask)

def nameScraper(soup):
    id_html = soup.find(id="8687fbccc611229100727249a775cc31")
    name = id_html.find('input', {'id': 'sc_task.request.requested_for_label'}).get("value").strip()
    print(name)
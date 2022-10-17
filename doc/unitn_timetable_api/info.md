# Unitn timetable API
Unitn provides some endpoints to fetch useful information about the timetable of the courses and classes. It seems there is not a description on how this enpoints work, so I tried to guess how they work.

## Endpoint to gather courses, teachers, and degrres /AgendaStudentiUnitn/combo.php
In this enpoint you can retrieve all the IDs necesssary to ask the other enpoints more information.
For example, if you want to download "Fundamental interactions" class schedule, you need to know its id. Just search for it in the json returned by this endpoint.

`https://easyacademy.unitn.it/AgendaStudentiUnitn/combo.php?sw=ec_&aa=2020&page=corsi`

> `sw=ec_` should mean _starts\_with_ = _ec\__, where _ec_ means _elective course_

You can choose between:
- Degree `page=corsi`
- Lecturer `page=docenti`
- Course `page=attivita`

The json received as a response will be different accordingly.

## Timetable endpoint /AgendaStudentiUnitn/grid_call.php
`https://easyacademy.unitn.it/AgendaStudentiUnitn/grid_call.php?view=easycourse&form-type=attivita&include=attivita&anno=2022&attivita%5B%5D=EC145660_IUPPA&visualizzazione_orario=cal&periodo_didattico=&date=10-10-2022&_lang=en&list=&week_grid_type=-1&ar_codes_=&ar_select_=&col_cells=0&empty_box=0&only_grid=0&highlighted_date=0&all_events=0&faculty_group=0&_lang=en&all_events=0&txtcurr=`

apparently it can be simplified as:
`https://easyacademy.unitn.it/AgendaStudentiUnitn/grid_call.php?view=easycourse&form-type=attivita&include=attivita&anno=2022&attivita%5B%5D=EC145660_IUPPA&visualizzazione_orario=cal&date=10-10-2022&list=&week_grid_type=-1&col_cells=0&empty_box=0&only_grid=0&highlighted_date=0&faculty_group=0&_lang=en&all_events=0`


## Endpoint to download full timetable in .ics AgendaStudentiUnitn/export/ec_download_ical_list.php
This is the full url used in the webapp:
`https://easyacademy.unitn.it/AgendaStudentiUnitn/export/ec_download_ical_list.php?view=easycourse&include=attivita&anno=2022&attivita%5B%5D=EC145660_IUPPA&visualizzazione_orario=cal&date=10-10-2022&_lang=en&highlighted_date=0&_lang=en&all_events=1&&_lang=en&ar_codes_=|EC145660_IUPPA&ar_select_=|true&txtaa=2022/2023&txtattivita=Fundamental%20Interactions%20%20[R.%20Iuppa]&corso=&cdl=&anno2=&docente=&txtcorso&txtanno&=&txtdocente=`
<br>

apparently it can be simplified just with this query parameters:
`https://easyacademy.unitn.it/AgendaStudentiUnitn/export/ec_download_ical_list.php?view=easycourse&include=attivita&anno=2022&attivita%5B%5D=EC145660_IUPPA&visualizzazione_orario=cal&date=10-10-2022&highlighted_date=0&all_events=1`
<br>

### URL query parameters
?
view=easycourse&<br>
include=attivita&<br>
anno=2022& **Year to gather**<br> 
attivita[]=EC145660_IUPPA& **Activity ID** <br> 
visualizzazione_orario=cal&<br>
date=10-10-2022&<br>
highlighted_date=0&<br>
all_events=1& **Set it to 1 to gather all the events in a year**

## Endpoint to download timetable in .xls /AgendaStudentiUnitn/export/ec_download_xls_list.php

import PySimpleGUI as sg
import guiFunctions as func


class MainWidget():
    sg.theme('GreenMono')  # Add a touch of color
    main_layout = [
        [sg.Text('Enter the URL you would like to add to your list'), sg.InputText()],
        [sg.Text('Enter the Name to Save the website as'), sg.InputText(), sg.Button('Add Website'),sg.Button('See list of websites')],
        [sg.Text('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')],
        [sg.Text('Enter the name of the website you would like to '
                                                        'delete from your files \n\t(once deleted you must re-enter to recieve updates)'), sg.InputText(), sg.Button('Delete')],
        [sg.Text(
            '-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')],
        [sg.Text('Press "Email Report" to scan and send a report to your inbox\n\t(A valid email address must be entered)'),sg.InputText(), sg.Button('Email Report')],
        [sg.Text('Press "Console Report" to display the report through a pop-up window.  Once a report is given, your website changes will reset to today.\n(This means that the changes will be lost unless you copy and paste them or send them to your email)'), sg.Button('Console Report')],
        [sg.Exit('Exit')]
        ]
    def __init__(self):
        error_close_duration = 3
        window = sg.Window('LilyScraper: The Best Free Tool For Tracking Websites', self.main_layout)
        #stuff inside the window
        # Create the Window
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.Read()
                #window for list of websites already stored
            if event in(None,'Exit'):
                break
            elif event in(None, 'See list of websites'):
                error_value,statement = func.list_of_items()
                if error_value == 1:
                    window_list = sg.PopupScrolled(statement, size = (65,30), title = f'Total Count: {func.number_of_items()}', auto_close= True, auto_close_duration=45)
                elif error_value ==2:
                    sg.popup_error(f'{statement}', title='ERROR', auto_close=True, auto_close_duration= 3)
            #button for adding website
            elif event in(None, 'Add Website'):
                try:
                    error_value,message = func.csv_list(str(values[1]).capitalize(), str(values[0]))
                    if error_value == 0:
                        sg.popup_error(f'{message}', title = 'Error!!', auto_close= True, auto_close_duration=45 )
                    elif error_value == 1:
                        sg.popup(f'{message}', title = 'Success!!')
                    elif error_value == 2:
                        sg.popup_error(f'{message}', title= 'ERROR!!', auto_close= True, auto_close_duration=45)
                        #error for when a correct link was entered but no html code could be grabbed
                    elif error_value == 3:
                        sg.popup_error(f'{message}', title= 'ERROR!!', auto_close= True, auto_close_duration=45)

                except: #handles error if incorrect name or link was entered or none at all
                    raise
                    sg.popup_error('Please Enter a correct name and link!!', title = 'ERROR', auto_close = True, auto_close_duration= error_close_duration )

            elif event in(None,'Delete'):
                name = values[2]
                error_value,statement = func.deleter(name)
                if error_value == 1:
                    sg.popup(f'{statement}', title = 'Success!!')
                elif error_value == 2:
                    sg.popup_error(f'{statement}', title = 'ERROR', auto_close= True,auto_close_duration= error_close_duration)
                elif error_value == 3:
                    sg.popup_error(f'{statement}', title='ERROR', auto_close=True, auto_close_duration= error_close_duration)


            elif event in(None, 'Email Report'):
                email = values[3]
                if '@' not in email or '.' not in email:
                    sg.popup_error('Make Sure you are entering your email correctly\nInclude the "@" and "."', title = 'ERROR', auto_close= True, auto_close_duration= error_close_duration)
                else:
                    error_value, statement = func.email_scanner(email)
                    if error_value == 1:
                        sg.popup_error(f'{statement}', title='ERROR', auto_close=True, auto_close_duration= error_close_duration)
                    elif error_value == 2:
                        sg.popup_error(f'{statement}', title='ERROR', auto_close=True, auto_close_duration= error_close_duration)
                    elif error_value == 3:
                        sg.popup_error(f'{statement}', title='ERROR', auto_close=True, auto_close_duration= error_close_duration)
                    elif error_value == 5:
                        sg.popup(f'{statement}', title = 'No Changes')
                    else:
                        sg.popup(f'{statement}', title='Success!!!')

            elif event in(None,'Console Report'):
                value, report = func.console_scanner()
                if value >= 1:
                    sg.PopupScrolled(report, title=f'Total Changes: {value}', auto_close=True, auto_close_duration= 45)
                elif value == -1:
                    sg.PopupScrolled(report, title=f'ERROR!', auto_close=True, auto_close_duration= 45)
                elif value == 0:
                    sg.popup(report, title='No Changes Found', auto_close=True, auto_close_duration= 45)
            if event == None and values == None:
                break
        window.close(); del window


if __name__ == '__main__':
    MainWidget()
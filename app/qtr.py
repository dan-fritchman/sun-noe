#
#
#
# def get_qtr_status(str_stat):
#     if str_stat in 'full yes '.split():
#         return Full()
#     elif str_stat in 'out no '.split():
#         return Out()
#     elif str_stat in 'half '.split():
#         return Half()
#     else:
#         return None
#
#
# @app.route('/<name>/quarter/<qname>/<status>')
# def update_qtr(name, status, qname='Quarter'):
#     print(f'Quarterly status update request for: {name} to {status}')
#
#     str_name = str(name).lower()
#     str_stat = str(status).lower()
#     str_qname = str(qname)
#
#     if str_name not in back_end.ids:
#         return f'SORRY we aint know no {name} '
#
#     sts = get_qtr_status(str_stat)
#     if sts is None:
#         return f'SORRY {name} didnt really understand {str_stat}'
#
#     if back_end.update_qtr(id=str_name, qtr=str_qname, status=sts.STATUS):
#         return render_template('response.html',
#                                STATUS=sts.STATUS,
#                                REPLY=sts.REPLY,
#                                DATA='')
#
#     return """SORRY something screwed up trying to update yo status.
#                        Maybe do it manually. """
#
#
#
#
# """
# Quarter-Status Polling Stuff
#  Really only been used once.
#  Maybe bring to more-general life, some day.
# """
#
#
# def qtr_status_msg(*, name, phone, qname, msg):
#     """ Send a full set of status links for quarter <qname> """
#
#     print(f'Sending quarter-status msg for {name}')
#     send_msg(phone=phone, body=msg)
#     time.sleep(1.0)
#
#     send_msg(phone=phone, body=os.environ['DOC_EDIT_URL'])
#     time.sleep(1.0)
#
#     for status in 'out half full '.split():
#         body = f'{app_url}/{name}/quarter/{qname}/{status}'
#         send_msg(phone=phone, body=body)
#         time.sleep(1.0)
#
#
# def poll_qtr(players, qname, msg):
#     for p in players:
#         name = p[0]
#         phone = p[1]
#         qtr_status_msg(name=name, phone=phone, qname=qname, msg=msg)
#
#
# def poll_q2():
#     """ Poll unknowns for the quarter """
#
#     u = get_unknowns(status_col='Q2_2018')
#     print(u)
#
#     to_poll = u
#     poll_qtr(players=to_poll,
#              qname='Q2_2018',
#              msg='Sunday BBall Q2 2018: ')
#

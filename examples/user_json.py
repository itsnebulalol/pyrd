from realdebrid import RealDebrid

rd = RealDebrid("TOKEN HERE")
print(rd.user.get().json())

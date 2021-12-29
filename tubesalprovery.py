"""
Ini adalah program yg dibuat menggunakan object oriented method, Rekursif dan juga loop
Disini saya membuat sebuah program olshop Dengan simulasi login
Yang menggunakan username dan  juga password.


Buyyer 

1. Bisa membeli barang dari seller
2. Melihat riwayat pembelian
3. Melihat barang2 yg dijual
4. Mengecek saldo

Seller

1. Bisa menambahkan barang jualan
2. Bisa menghapus barang jualan
3. Melihat barang jualan
4. Mengecek pendapatan
"""

User = []
listbarang = []

def rupiah(h):
	return "{0:,}".format(h).replace(",", ".")

#Fungsi untuk get barang
def getBarang(barang):
	for x in listbarang:
		if x.getName() == barang:
			return x
	return None

#Fungsi untuk mencari user
def getUser(nama, password):
	for x in User:
		if x.getName() == nama:
			if x.getPassword() == password:
				return x
	print("Nama atau password salah.")
	return None

#Object Login sebagai base
class Login():
	
	def __init__(self, username, password):
		self.username = username
		self.password = password
	
	#Fungsi pengambilan username
	def getName(self):
		return self.username
	
	#Fungsi pengambilan password
	def getPassword(self):
		return self.password

#Object Biyyer turunan login
class Buyyer(Login):
	
	def __init__(self, user):
		self.user = user
		self.username = user.getName()
		self.password = user.getPassword()
		self.saldo = int(input("Masukkan saldo anda: "))
		self.riwayat = {}
	
	#Untuk mengecek sisa saldo
	def cekSaldo(self):
		return "Total saldo anda: Rp.{0:,}".format(self.saldo).replace(",", ".")
	
	#Fungsi pembelian barang dengan loop
	def beliBarang(self):
		barang = input("Masukkan nama barang: ").lower()
		if barang == "exit":
			return self.menu()
		a = getBarang(barang)
		if not a:
			print("Barang tidak terdaftar dalam list")
			return self.beliBarang()
		x = False
		while not x:
			jumlah = int(input("Masukkan jumlah barang, Ketik 0 untuk kembali ke menu utama: "))
			if jumlah > a.getStock():
				print("Stock barang tidak cukup")
				continue
			if jumlah == 0:
				self.menu()
			if self.saldo < jumlah*a.getHarga():
				print("Saldo tidak cukup")
				return self.menu()
			a.stock -= jumlah
			harga = a.getHarga()
			a.seller().pendapatan += jumlah*harga
			self.riwayat[a.getName()] = {"jumlah": jumlah, "harga": harga*jumlah, "penjual": a.user.getName()}
			x = True
			print("Berhasil membeli barang")
		return self.menu()
	
	#Untuk menampilkan barang jualan
	def barang2(self):
		if listbarang == []:
			print("Belum ada yg menjual barang")
		ret = "No.	Nama		Harga		Stock		Penjual\n\n"
		no = 0
		for x in listbarang:
			no += 1
			ret += f"{no}.	{x.getName()}	Rp.{rupiah(x.getHarga())}	{x.getStock()}	{x.user.getName()}\n"
		ret += "\n	By Kelompok 14"
		print(ret)
		return self.menu()
	
	#Untuk menampilkan riwayat pembelian
	def riwayatPembelian(self):
		if self.riwayat == {}:
			print("Tidak ada riwayat pembelian")
		ret = "	Riwayat Pembelian\n\n"
		no = 0
		for x in self.riwayat:
			no += 1
			ret += "{}. Nama: {}	Jumlah: {}	Harga: Rp.{}	Penjual: {}\n".format(no, x, x["jumlah"], rupiah(x["harga"]), x["penjual"])
		ret += "\n	By Kelompok 14"
		print(ret)
		return self.menu()
	
	#Menu dari object buyyer
	def menu(self):
		ret = """
	Buyyer Menu

1. Buy Product
2. List Product
3. Cek Saldo
4. Riwayat pembelian
5. Logout

		"""
		print(ret)
		ans = int(input("Masukkan angka"))
		if ans == 1:
			self.beliBarang()
		elif ans == 2:
			self.barang2()
		elif ans == 3:
			print(self.cekSaldo())
			self.menu()
		elif ans == 4:
			self.riwayatPembelian()
		elif ans == 5:
			main()
		else:
			self.menu()

#Object seller Turunan login
class Seller(Login):
	
	def __init__(self, user):
		self.user = user
		self.username = user.getName()
		self.password = user.getPassword()
		self.pendapatan = 0
	
	#Untuk mengecek pendapatan
	def getPendapatan(self):
		return "Rp.{0:,}".format(self.pendapatan).replace(",", ".")
	
	#Untuk menambah barang jualan
	def tambahBarang(self):
		nama = input("Masukkan nama barang atau exit untuk kembali ke menu utama: ")
		if nama == "exit":
			return self.menu()
		a = getBarang(nama)
		if a:
			print("Barang sudah ada")
			return self.tambahBarang()
		x = False
		while not x:
			harga = input("Masukkan harga atau ketik 00 untuk mebmbatalkan: ")
			if "00" == harga:
				return self.menu()
			if int(harga) <= 0:
				print("Harga tidak boleh kurang dari sama dengan 0")
				continue
			harga = int(harga)
			x = True
		while x:
			stock = input("Masukkan jumah stock atau ketik 00 untuk kembali: ")
			if "00" in stock:
				return self.menu()
			if int(stock) <= 0:
				print("Stock tidak boleh kurang dari sama dengan 0")
				continue
			stock = int(stock)
			x = False
		barang = Product(nama, harga, stock, self.user)
		listbarang.append(barang)
		print("Success add barang baru untuk dijual")
		return self.menu()
	
	#Untuk melihat barang jualan
	def lihatJualan(self):
		barang = []
		for x in listbarang:
			if x.seller().getName() == self.getName():
				barang.append(x)
		if barang == []:
			print("Kamu belum menjual barang apapun.")
			return self.menu()
		ret = "No.	Nama	Harga	Stock\n\n"
		no = 0
		for xx in barang:
			no += 1
			ret += f"{no}.	{xx.getName()}	Rp.{rupiah(xx.getHarga())}	{xx.getStock()}\n"
		ret += "\n	By Kelompok 14"
		print(ret)
		return self.menu()
	
	#Untuk menghapus barang dri list
	def hapusBarang():
		barang = input("Masukkan nama barang: ")
		if barang == "exit":
			return self.menu()
		a = getBarang(barang)
		if not a:
			print("Nama tidak tersedia")
			return self.hapusBarang()
		if a.seller().getName() != self.getName():
			print("Bukan barang yang anda jual")
			return self.hapusBarang()
		while True:
			decide = input("Apakah anda yakin ingin menghapus (y/n): ")
			if decide == "y":
				listbarang.remove(a)
				print("Success remove barang")
				return self.menu()
			elif decide == "n":
				print('Kembali ke menu utama.')
				return self.menu()
			else:
				print("Tidak ada jawaban seperti "+decide)
	
	#Menu utama object seller
	def menu(self):
		ret = """
	Seller Menu

1. Tambahkan barang
2. Hapus barang
3. Lihat barang jualan
4. Total penjualan
5. Logout
	
	By Kelompok 14
		"""
		print(ret)
		ans = int(input("Masukkan angka dari menu: "))
		if ans == 1:
			self.tambahBarang()
		elif ans == 2:
			self.hapusBarang()
		elif ans == 3:
			self.lihatJualan()
		elif ans == 4:
			print("Total pendapatan anda: "+self.getPendapatan())
			self.menu()
		elif ans == 5:
			main()
		else:
			self.menu()

class Product():
	
	def __init__(self, nama, harga, stock, user):
		self.nama = nama
		self.harga = harga #int(input("Silahkan tentukan harga: "))
		self.stock = stock #int(input("Silahkan masukkan jumlah stock"))
		self.user = user
	
	#Nama barang
	def getName(self):
		return self.nama
	
	#Jumlah stock barang
	def getStock(self):
		return self.stock
	
	#Harga barang
	def getHarga(self):
		return self.harga
	
	#Fungsi mencari pwnjual barang
	def seller(self):
		return getUser(self.user.getName(), self.user.getPassword())

#Pembuatan akun
def signUp():
	try:
		nama = input("Masukkan nama: ")
		for x in User:
			if x.getName == nama:
				print("Already in use")
				return signUp()
		password = input("Masukkan password: ")
		client = Login(nama, password)
		x = False
		while not x:
			tipe = input("Masukkan type (seller/buyyer): ").lower()
			if tipe not in ["seller", "buyyer"]:
				continue
			if tipe == "seller":
				cl = Seller(client)
			elif tipe == "buyyer":
				cl = Buyyer(client)
			User.append(cl)
			print("Success sign up")
			return main()
	except KeyboardInterrupt:
		main()

#Main menu
def main():
	try:
		ret = """
	Main Menu

1. Signup
2. Login
3. Exit
		"""
		print(ret)
		ans = int(input("Masukkan angka: "))
		if ans == 1:
			signUp()
		elif ans == 2:
			x = False
			while not x:
				unam = input("Masukkan username: ")
				password = input("Masukkan password: ")
				a = getUser(unam, password)
				if not a:
					continue
				x = True
			a.menu()
		elif ans == 3:
			sys.exit()
		else:
			main()
	except KeyboardInterrupt:
		sys.exit()

main()

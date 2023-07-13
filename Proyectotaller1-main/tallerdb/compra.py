class Carrito:
	def __init__(self, request ):
		self.request = request
		self.session = request.session
		carrito = self.session.get("carrito")
		if not carrito:
			carrito = self.session["carrito"] = {}
		self.carrito=carrito

	def agregar(self, producto):
		if producto.id_producto not in self.carrito.keys():
			self.carrito[producto.id_producto]={
				"id_producto":producto.id_producto,
				"nombre": producto.nombre,
				"precio": str (producto.precio),
				"cantidad": 1,
				"total": producto.precio,

    }
		else: 
			for key, value in self.carrito.items():
				if key==producto.id_producto:
					value["cantidad"] = value["cantidad"]+1
					value["precio"] = producto.precio
					value["total"]= value["total"] + producto.precio
					break
		self.guardar_carrito()

	def guardar_carrito(self):
		self.session["carrito"] = self.carrito
		self.session.modified=True
		
	def eliminar(self, producto):
		id = producto.id_producto
		if id in self.carrito:
			del self.carrito[id]
			self.guardar_carrito()

	def restar (self, producto):
		id = str(producto.id_producto)
		if id in self.carrito.keys():
			self.carrito[id]["cantidad"] -=1
			self.carrito[id]["total"] -= producto.precio
			if self.carrito[id]["cantidad"] <= 0: self.eliminar(producto)
			self.guardar_carrito()
	    
	def limpiar(self):
		self.session["carrito"]={}
		self.session.modified=True
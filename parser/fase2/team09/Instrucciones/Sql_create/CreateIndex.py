from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.Excepcion import Excepcion
from Instrucciones.TablaSimbolos.Tipo import Tipo, Tipo_Dato

class CreateIndex(Instruccion):
    def __init__(self, unique, nombre, tabla, using, campos, condicion, strGram, linea, columna):
        Instruccion.__init__(self, None, linea, columna, strGram)
        self.unique = unique
        self.nombre = nombre
        self.tabla = tabla
        self.using = using
        self.campos = campos
        self.condicion = condicion
        self.tipo = Tipo(Tipo_Dato.INDEX)
        self.constraint = None

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla, arbol)
        restricciones = " "
        self.unique = self.unique.ejecutar(tabla, arbol)
        if self.unique is not None:
            restricciones = restricciones + self.unique
            self.constraint = []
        self.using = self.using.ejecutar(tabla, arbol)
        if self.using is not None:
            if self.unique is None:
                restricciones = restricciones + self.using
            else:
                restricciones = restricciones + ", " + self.using
            self.constraint = []
        restricciones = restricciones
        if self.constraint is not None:
            self.constraint.append(Cons(restricciones, "restricciones"))
        err = False
        exi = False
        restricciones = ""
        for db in arbol.listaBd:
            for t in db.tablas:
                if t.nombreDeTabla == self.tabla:
                    for c in t.lista_de_campos:
                        if c.tipo.toString() == "index":
                            if c.nombre == self.nombre:
                                error = Excepcion('INX00', "Semántico", "Ya existe un índice llamado «" + self.nombre + "» en la tabla «" + self.tabla + "»", self.linea, self.columna)
                                arbol.excepciones.append(error)
                                arbol.consola.append(error.toString())
                                err = True
                                break
                        else:
                            for l in self.campos:
                                if c.nombre == l.nombre:
                                    if not l.existe:
                                        l.existe = True
                    for l in self.campos:
                        if l.existe:
                            restricciones = restricciones + " " + l.nombre + l.ejecutar(tabla, arbol)
                        else:
                            l.ejecutar(tabla, arbol)
                            error = Excepcion("INX01", "Semántico", "No existe el campo «" + l.nombre + "» en la tabla «" + self.tabla + "»", self.linea, self.columna)
                            arbol.excepciones.append(error)
                            arbol.consola.append(error.toString())
                            err = True
                        for w in self.campos:
                            if l != w and not w.dupli and l.nombre == w.nombre:
                                error = Excepcion("INX02", "Semántico", "Ya existe el campo «" + l.nombre + "» en el índice", self.linea, self.columna)
                                arbol.excepciones.append(error)
                                arbol.consola.append(error.toString())
                                err = True
                                l.dupli = True
                                break
                    if not err:
                        if self.constraint is None:
                            self.constraint = []
                            self.constraint.append(Cons(restricciones, "campo(s)"))
                        else:
                            self.constraint.append(Cons(restricciones, "<br>campos(s)"))
                        t.lista_de_campos.append(self)

class Cons():
    def __init__(self, id, rindex):
        self.id = id
        self.rindex = rindex
        
    def toString(self):
        if self.rindex is not None:
            return self.rindex
        return ""      

# coding=utf-8

# Yacc example
from ply.lex import lex
from ply.yacc import yacc

# Get the token map from the lexer.  This is required.
from lexer_rules import *
from parser_rules import *

data = []

data.append(('''
x = 1;
if (x + 2) {x= 2+3;y=2+1; #hola
}
''',
'''x = 1;
if (x + 2) {
	x = 2 + 3;
	y = 2 + 1; #hola
}
'''
,1, True))

data.append(('''
while(true) {x= 2+3;y=2+1; #hola
}
''',
'''while (true) {
	x = 2 + 3;
	y = 2 + 1; #hola
}
'''
,2, True))

data.append(('''
x = 3;
if (x + 2) { x = 1 +2;

}
''',
'''x = 3;
if (x + 2) {
	x = 1 + 2;
}
'''
,3, True))

data.append(('''
while(true) x = 2;
''',
'''while (true)
	x = 2;
'''
,4, True))

data.append(('''x=1;
for(;x<0;x=x-1)
x = 2;
''',
'''x = 1;
for (; x < 0; x = x - 1)
	x = 2;
'''
,5, True))

data.append(('''
for(x=1;x<0;x=x-1) #hola
	#chau
	x = 2;
''',
'''for (x = 1; x < 0; x = x - 1)
	#hola
	#chau
	x = 2;
'''
,6, True))

data.append(('''
if(false) #hola
x = 2; else #hola
y=3;
''',
'''if (false)
	#hola
	x = 2;
else
	#hola
	y = 3;
'''
,7, True))

data.append(('''
if(false) { #hola
x = 2; } else { #hola
y=3;}
''',
'''if (false) {
	#hola
	x = 2;
}
else {
	#hola
	y = 3;
}
'''
,8, True))

data.append(('''
if(false) #hola
x = 2; y=3; z = 1;
''',
'''if (false)
	#hola
	x = 2;
y = 3;
z = 1;
'''
,9, True))

data.append(('''y=3;
do{x=y+1;}
while(y<1); t = y; return ;
''',
'''y = 3;
do {
	x = y + 1;
} while (y < 1);
t = y;
return;
'''
,10, True))

data.append(('''
siete = false;
hola = [1, 2, 3][2];
f = false;
x = "y";
y = "x";
campo = [{campo:"1"}, {campo:"2"}, {campo:"3"}][1];
campo = {e:2, eda:["a"][2 + 4], A:8.5};
a = {nombre:"Jose", edad:length("hola")};
b = 10;
j = "";
g = 6;
c = 1.1;
dos = 2 > 2;
print({ca:["1", "2", "4"][5]}.ca);
algo = true;
no = false;
amarillo = [true, true][2];
if ([false][{m:2}.m] == (b > 10))
	while (5 > 10)
		for (; true; ) {
			#AA#AA
			if (f) {
print(x + "x");
			} else {
				do
print("y" + y);
while (1 == 1);
				aa = true AND false;
				bb = NOT aa;
			}
			print({dos:[1, 2, 3][2 * 3]}.dos + {e:"a", j:j, r:5.5}.r);
		}
if (algo)
if (no)
print(2);
else
x = 3;
while (amarillo)
do
#NADA
#DE
#NADA
z = [a.edad + length("doce" + capitalizar("2")) / 2, 1.0 + (siete ? ((aa OR bb AND (2 != length("")) ? 1 : 2)) : g * 12 % 3), NOT aa ? b / -5 : c];
while (dos);
''',

'''siete = false;
hola = [1, 2, 3][2];
f = false;
x = "y";
y = "x";
campo = [{campo:"1"}, {campo:"2"}, {campo:"3"}][1];
campo = {e:2, eda:["a"][2 + 4], A:8.5};
a = {nombre:"Jose", edad:length("hola")};
b = 10;
j = "";
g = 6;
c = 1.1;
dos = 2 > 2;
print({ca:["1", "2", "4"][5]}.ca);
algo = true;
no = false;
amarillo = [true, true][2];
if ([false][{m:2}.m] == (b > 10))
	while (5 > 10)
		for (; true; ) {
			#AA#AA
			if (f) {
				print(x + "x");
			}
			else {
				do
					print("y" + y);
				while (1 == 1);
				aa = true AND false;
				bb = NOT aa;
			}
			print({dos:[1, 2, 3][2 * 3]}.dos + {e:"a", j:j, r:5.5}.r);
		}
if (algo)
	if (no)
		print(2);
	else
		x = 3;
while (amarillo)
	do
		#NADA
		#DE
		#NADA
		z = [a.edad + length("doce" + capitalizar("2")) / 2, 1.0 + (siete ? ((aa OR bb AND (2 != length("")) ? 1 : 2)) : g * 12 % 3), NOT aa ? b / -5 : c];
	while (dos);
'''
,11, True))

data.append(('''
i = 0;
while(true)
#Comentario antes del if
if (i<2)
{
#Algo sobre el then del if
valores[i]=i;
i++;}
else
#Algo sobre el else
valores[i] = valores[i-1]+valores[i-2];
res = valores;
''', 
'''i = 0;
while (true)
	#Comentario antes del if
	if (i < 2) {
		#Algo sobre el then del if
		valores[i] = i;
		i++;
	}
	else
		#Algo sobre el else
		valores[i] = valores[i - 1] + valores[i - 2];
res = valores;
'''
, 12, True))

data.append(('''
a = 0;
b = 1;
a = b;
c = 2.5;
d = "Hola";
e = d;

f = [1, 2, 3];
a = f[1];
b = f[2];

g = [1, a, 2, b, 3];
g[a] = b;
g[b] = a;

h = [f[g[a]], g[g[b]]];
h[f[g[a]]] = g[f[g[g[b]]]];

c1 = "2+2=4;";
c2 = "if (c) then ... else ...";
c3 = "# Este no es un comentario";
''', 
'''a = 0;
b = 1;
a = b;
c = 2.5;
d = "Hola";
e = d;
f = [1, 2, 3];
a = f[1];
b = f[2];
g = [1, a, 2, b, 3];
g[a] = b;
g[b] = a;
h = [f[g[a]], g[g[b]]];
h[f[g[a]]] = g[f[g[g[b]]]];
c1 = "2+2=4;";
c2 = "if (c) then ... else ...";
c3 = "# Este no es un comentario";
'''
, 13, True))


data.append(('''a = true;
b = false;
c = a AND b;
d = NOT false;
e = d OR false;
f = c == b;
g = (a != c);

x = 5;
y = 10;
h = (e AND false) OR ((x < 1) == (y > 2));
i = NOT f ? (x > 5 ? y : 10) : x + 5;

j = [true, false];
k = [1, 2, 3];

l = j[1] ? (k[1] == k[3]) : j[2] == a ? b : c;
m = ((x + k[2] > 3) ? 2 ^ k[0] : (j[2] ? k[1] + 6 : (y)));
''',
'''a = true;
b = false;
c = a AND b;
d = NOT false;
e = d OR false;
f = c == b;
g = (a != c);
x = 5;
y = 10;
h = (e AND false) OR ((x < 1) == (y > 2));
i = NOT f ? (x > 5 ? y : 10) : x + 5;
j = [true, false];
k = [1, 2, 3];
l = j[1] ? (k[1] == k[3]) : j[2] == a ? b : c;
m = ((x + k[2] > 3) ? 2 ^ k[0] : (j[2] ? k[1] + 6 : (y)));
'''
, 14, True))


data.append(('''# Principio

# Primera instrucción, por cierto: 2 + 2 = 4;
	a = 0;

# Segunda instrucción, ¿sabías que "true AND false" != "true OR false"?
	b = 1;	# Medio

# Tercera instrucción: if (c) then ... else ...
	c = 10;

# Fin

''',
'''# Principio
# Primera instrucción, por cierto: 2 + 2 = 4;
a = 0;
# Segunda instrucción, ¿sabías que "true AND false" != "true OR false"?
b = 1; # Medio
# Tercera instrucción: if (c) then ... else ...
c = 10;
# Fin
'''
, 15, True))


data.append(('''for (a=0; a<10; a++)
	d = 1;

for (; true; ) {
	# Co
	# men
	# tario
	b = 2;
	c = 3;
}

for (d = b; b != c; a = b)
	# Co
	# men
	# tario
	e = 10;

for (b = false ? c + d : a; a + b + c == d - e -d; ) {a = d; d=a;}
for (; a + b + c == d - e -d; b = false ? c + d : a) a = d; d=a;

if (false)
for (; true; )
for (; false; ) {
if (true)
if (false) {
f = "donde estoy?";
}
else {
for (c = b; b > c; b = c)
a = a;
}
}
else
for (; true; )
f = "NO";
''',
'''for (a = 0; a < 10; a++)
	d = 1;
for (; true; ) {
	# Co
	# men
	# tario
	b = 2;
	c = 3;
}
for (d = b; b != c; a = b)
	# Co
	# men
	# tario
	e = 10;
for (b = false ? c + d : a; a + b + c == d - e - d; ) {
	a = d;
	d = a;
}
for (; a + b + c == d - e - d; b = false ? c + d : a)
	a = d;
d = a;
if (false)
	for (; true; )
		for (; false; ) {
			if (true)
				if (false) {
					f = "donde estoy?";
				}
				else {
					for (c = b; b > c; b = c)
						a = a;
				}
		}
else
	for (; true; )
		f = "NO";
'''
, 16, True))

data.append(('''a = 10;
b = [a];
c = [1, 2, 3];

print(a);
print("Hola");
print(c);
print((1 > 2 ? "Mun" + "do" : "a todos") + "!");

d = length(b);
length("IDLE");
print(length(c) + 5);

capitalizar("-");
e = length(capitalizar("MAYUSCULAS"));
print(capitalizar("m" + "M"));

colineales(b, c);
print(capitalizar(colineales(b, c) ? "B" : "C"));

multiplicacionEscalar(b, a);
print(length([1, length(multiplicacionEscalar(b, a, colineales(c,c))), length(capitalizar("2"))]));
''',
'''a = 10;
b = [a];
c = [1, 2, 3];
print(a);
print("Hola");
print(c);
print((1 > 2 ? "Mun" + "do" : "a todos") + "!");
d = length(b);
length("IDLE");
print(length(c) + 5);
capitalizar("-");
e = length(capitalizar("MAYUSCULAS"));
print(capitalizar("m" + "M"));
colineales(b, c);
print(capitalizar(colineales(b, c) ? "B" : "C"));
multiplicacionEscalar(b, a);
print(length([1, length(multiplicacionEscalar(b, a, colineales(c, c))), length(capitalizar("2"))]));
'''
, 17, True))


data.append(('''if (true)
	a = 1;

if (NOT (6 == 5) != (false ? false : false)) {
	# Co
	# men
	# tario
	b = 2;
	c = 3;
}

if (b != c)
	# Co
	# men
	# tario
	d = 10;
else
	e = 5;

if (a + b + c == d - e -d) {a = d;} else {d = a;}

if (false)
if (true)
if (false) {
if (true)
if (false) {
f = "donde estoy?";
}
else {
if (b > c)
a = a;
}
} else
if (b < c) {
d = e;
} else {
e = d;
}
else
f = "YES";
else
f = "NO";
''',
'''if (true)
	a = 1;
if (NOT (6 == 5) != (false ? false : false)) {
	# Co
	# men
	# tario
	b = 2;
	c = 3;
}
if (b != c)
	# Co
	# men
	# tario
	d = 10;
else
	e = 5;
if (a + b + c == d - e - d) {
	a = d;
}
else {
	d = a;
}
if (false)
	if (true)
		if (false) {
			if (true)
				if (false) {
					f = "donde estoy?";
				}
				else {
					if (b > c)
						a = a;
				}
		}
		else
			if (b < c) {
				d = e;
			}
			else {
				e = d;
			}
	else
		f = "YES";
else
	f = "NO";
'''
, 18, True))

data.append(('''a = -10;
b = 2 + 3 - 8 + 1;
c = 3 * 5 % 4 / 6;
d = 2.0 ^ 9.0;
e = -3 * (4 / ((3) + 8 ^ ((1))) - -5 + -(7) * 6);

f = -a * (b / ((a) + d ^ ((c))) - -b + -(c) * a);

g = [1.5, 2 * (7) + 5 / 0, a * d, 8 ^ 1.0, (6) / (6), (3 + 3) + 0.0, e - 5, 2 * -f];
h = [1,b,3];

g[2 * 4] = 10 + (3 * 2/1);
g[b ^ b] = (g[7 * (5) + (h[(2)])]);
g[9 - (5 % 3)] = g[b % h[b]];

a += b;
c *= e / f;
g[b] /= 1 + g[1];
--f;
g[4]++;
''',
'''a = -10;
b = 2 + 3 - 8 + 1;
c = 3 * 5 % 4 / 6;
d = 2.0 ^ 9.0;
e = -3 * (4 / ((3) + 8 ^ ((1))) - -5 + -(7) * 6);
f = -a * (b / ((a) + d ^ ((c))) - -b + -(c) * a);
g = [1.5, 2 * (7) + 5 / 0, a * d, 8 ^ 1.0, (6) / (6), (3 + 3) + 0.0, e - 5, 2 * -f];
h = [1, b, 3];
g[2 * 4] = 10 + (3 * 2 / 1);
g[b ^ b] = (g[7 * (5) + (h[(2)])]);
g[9 - (5 % 3)] = g[b % h[b]];
a += b;
c *= e / f;
g[b] /= 1 + g[1];
--f;
g[4]++;
'''
, 19, True))


data.append(('''usuario = {nombre:"Al", edad:50};
print(capitalizar(usuario.nombre));
nacimiento = 2016;
nacimiento -= usuario.edad;
usuarios = [{nombre:"Mr.X", edad:10}, usuario];

suma = 0;
for (i = 0; i < length(usuarios); i++) {
	print(usuarios[i].nombre);
	suma += usuarios[i].edad;
}

j = [[1],[2],[1, 2, 3]];
k = {list:["A", "B", "c"], doublelist:j};
a = 0;
a += k.doublelist[0][1];
''',
'''usuario = {nombre:"Al", edad:50};
print(capitalizar(usuario.nombre));
nacimiento = 2016;
nacimiento -= usuario.edad;
usuarios = [{nombre:"Mr.X", edad:10}, usuario];
suma = 0;
for (i = 0; i < length(usuarios); i++) {
	print(usuarios[i].nombre);
	suma += usuarios[i].edad;
}
j = [[1], [2], [1, 2, 3]];
k = {list:["A", "B", "c"], doublelist:j};
a = 0;
a += k.doublelist[0][1];
'''
, 20, True))


data.append(('''		

			a =
0		;

	b= 1;		c=10;d=	5

	;	

		
''',
'''a = 0;
b = 1;
c = 10;
d = 5;
'''
, 21, True))

data.append(('''while (true) {
	d = 1;
	a = 0;
}

do {
	# Co
	# men
	# tario
	b = 2;
	c = 3;
} while ((d > 10) AND NOT false);

while (b != c)
	# Co
	# men
	# tario
	e = 10;

do
	a = d;
while (false);

do
	while (a + b + c == d - e)
		a = d;
while (d > a);

if (false)
for (; true; )
do {
while (true)
if (false) {
f = "donde estoy?";
}
else {
for (c = b; b > c; b = c)
while (true)
a = a;
}
} while (b > 1 ? false : true OR false);
else
for (; true; )
while (false)
f = "NO";
''',
'''while (true) {
	d = 1;
	a = 0;
}
do {
	# Co
	# men
	# tario
	b = 2;
	c = 3;
} while ((d > 10) AND NOT false);
while (b != c)
	# Co
	# men
	# tario
	e = 10;
do
	a = d;
while (false);
do
	while (a + b + c == d - e)
		a = d;
while (d > a);
if (false)
	for (; true; )
		do {
			while (true)
				if (false) {
					f = "donde estoy?";
				}
				else {
					for (c = b; b > c; b = c)
						while (true)
							a = a;
				}
		} while (b > 1 ? false : true OR false);
else
	for (; true; )
		while (false)
			f = "NO";
'''
, 22, True))


data.append(('''y = 3;
x = "hola";
z = x + y;
''',
'''
'''
, 23, False))

data.append(('''
a = [[1, 2, 3], ["hola", "chau"]];
''',
'''
'''
, 24, False))

data.append(('''
a = {x:[1, 2, 3], y:["hola", "chau"]};
z = x[1] + "hola";
''',
'''
'''
, 25, False))

data.append(('''
a = {x:[1, 2, 3], y:["hola", "chau"]};
z = a.x[1] + a.y[2];
''',
'''
'''
, 26, False))

data.append(('''
a = [[[1, 2, 3], [1, 2]], [["hola"]]];
''',
'''
'''
, 27, False))

data.append(('''
a = (multiplicacionEscalar([1,2.2,3],3,true))[0] + 3;
''',
'''a = (multiplicacionEscalar([1, 2.2, 3], 3, true))[0] + 3;
'''
, 28, True))

data.append(('''
a = (multiplicacionEscalar([1,2.2,3],3,true))[0] + colineales([1,2],[3,4]);
''',
'''
'''
, 29, False))

data.append(('''
a = +("hola");
''',
'''
'''
, 29, False))

data.append(('''
vector = [1, 3, 4];
a = +(vector["1"]);
''',
'''
'''
, 29, False))

	
# Build the parser
import sys
import difflib

parser = yacc()
lexer = lex()


for i in range(0, len(data)):
	lexer.lineno = 0 # Reset de los numeros de linea del lexer.
	types.clear()    # Importante limpiear los tipos!
	registers.clear()

	try:
		result = parser.parse(data[i][0], lexer)
	except SyntaxError as e:
		print("Test " + str(data[i][2]) + ": fallo!")
		print("input:")
		print(data[i][0])
		print(e)
		break
	except TypeError as e:
		if (not data[i][3]):
			print("Test " + str(data[i][2]) + ": paso! error: " + str(e))
			continue
		else:
			print("Test " + str(data[i][2]) + ": fallo!")
			print("input:")
			print(data[i][0])
			print(e)
			break

	if (not data[i][3]):
		print("Test " + str(data[i][2]) + ": fallo!")
		print("input:")
		print(data[i][0])
		print("Deberia haber dado un error de tipo!!")
		break

	if (not data[i][1] == result.formatted_code):
		print("Test " + str(data[i][2]) + ": fallo!")

		print("input:")
		print(data[i][0])

		print("esperado:")
		print(data[i][1])

		print("output:")
		print(result.formatted_code)

		fe = open('test_expected.txt', 'w')
		fo = open('test_output.txt', 'w')
		fe.truncate()
		fo.truncate()

		fe.write(data[i][1])
		fo.write(result.formatted_code)

		if (not data[i][1] == ""):
			a = data[i][1]
			b = result.formatted_code
			for i,s in enumerate(difflib.ndiff(a, b)):
				if s[0]==' ': continue
				elif s[0]=='-':
					print(u'Delete "{}" from position {}'.format(s[-1],i))
				elif s[0]=='+':
					print(u'Add "{}" to position {}'.format(s[-1],i))
			print()
			if (not a == b):
				sys.exit("ERROR! El output no es el esperado")
		else:
			sys.exit("ERROR! No hay string para comparar")

		break
	else:
		print("Test " + str(data[i][2]) + ": paso!")

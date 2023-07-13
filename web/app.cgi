#!/usr/bin/python3

#from os import environ
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request, redirect
import psycopg2
import psycopg2.extras


# SGBD configs

DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "ist199066"
DB_DATABASE = DB_USER
DB_PASSWORD = "dlce5059"
"""
DB_HOST = "localhost"
DB_USER = "postgres"
DB_DATABASE = DB_USER
DB_PASSWORD = "my_secret_pw"
"""
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (
	DB_HOST,
	DB_DATABASE,
	DB_USER,
	DB_PASSWORD,
)

app = Flask(__name__)

#user = "/./"
user = "/ist199066/app.cgi"

@app.context_processor
def user_select():
    return dict(user=user)

# environ['SERVER_NAME'] = ""

@app.route("/")
def root():
	return redirect(user+"/cat")

@app.route("/cat")
def list_categories():
	dbConn = None
	cursor = None
	cursor_s = None
	s_cursor = None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor_s = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "SELECT nome FROM categoria_simples;"
		cursor_s.execute(query)
		s_cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "SELECT nome FROM super_categoria;"
		s_cursor.execute(query)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "SELECT nome FROM categoria;"
		cursor.execute(query)
		return render_template("index.html", cats_s=cursor_s, s_cats=s_cursor, cats = cursor)
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		cursor_s.close()
		s_cursor.close()
		cursor.close()
		dbConn.close()

@app.route("/add_cat")
def add_cat():
		return render_template("add_cat.html")

@app.route("/add_cat",methods=["POST"])
def add_c():
	dbConn = None
	cursor = None
	novo = request.form["novo"]
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "INSERT INTO categoria_simples VALUES %(nome)s;"
		cursor.execute(query,{'nome':(novo,)})
		return redirect(user + "/")
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route("/del/<cat>")
def dcat(cat):

	def rlinks(cat):
		dbConn = None
		cursor = None
		try:
			dbConn = psycopg2.connect(DB_CONNECTION_STRING)
			cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
			query = f"""
		WITH RECURSIVE subcategorias AS (
			SELECT
				categoria,
				super_categoria
			FROM
				tem_outra
			WHERE
				super_categoria = %(nome)s OR categoria = %(nome)s
		UNION
				SELECT
					e.categoria,
					e.super_categoria
				FROM
					tem_outra e
				INNER JOIN subcategorias s ON s.categoria = e.super_categoria
		) DELETE FROM tem_outra WHERE categoria IN (
			SELECT categoria FROM subcategorias) 
			AND super_categoria IN (
				SELECT super_categoria FROM subcategorias 
				WHERE categoria = categoria);
		"""
			cursor.execute(query,{'nome':cat})
		except Exception as e:
			return str(e)  # Renders a page with the error.
		finally:
			dbConn.commit()
			cursor.close()
			dbConn.close()

	dbConn = None
	cursor = None
	rlinks(cat)
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		# query = "DELETE FROM categoria WHERE nome =  %(nome)s;"
		query = f"""
			DELETE FROM tem_categoria
			WHERE nome = %(cat)s;


			DELETE FROM responsavel_por
			WHERE nome_cat = %(cat)s;


			DELETE FROM categoria_simples
			WHERE nome = %(cat)s;

			DELETE FROM super_categoria
			WHERE nome = %(cat)s;
			
			"""
		data = (cat,)
		cursor.execute(query,{'cat':data})
		return redirect(user + "/")
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route("/cat/<cat>")
def cat(cat):
	dbConn = None
	cursor = None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "SELECT nome FROM super_categoria WHERE nome = %(nome)s"
		cursor.execute(query,{'nome':(cat,)})
		if(cursor.fetchone()==None):
			return redirect(user + "/")
		query = f"""
		WITH RECURSIVE subcategorias AS (
			SELECT
				categoria,
				super_categoria
			FROM
				tem_outra
			WHERE
				super_categoria = %(nome)s
			UNION
				SELECT
					e.categoria,
					e.super_categoria
				FROM
					tem_outra e
				INNER JOIN subcategorias s ON s.categoria = e.super_categoria
		) SELECT
			*
		FROM
			subcategorias;
		"""
		cursor.execute(query,{'nome':(cat,)})
		return render_template("cat.html", cats=cursor,supercat=cat)
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		cursor.close()
		dbConn.close()


@app.route("/add_sub")
def add_sub():
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor1 = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor_r = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "SELECT * FROM categoria"
		query_r = "SELECT * FROM tem_outra"
		cursor.execute(query)
		cursor1.execute(query)
		cursor_r.execute(query_r)
		return render_template("add_sub.html",cats1=cursor1,cats=cursor,rels=cursor_r)
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		cursor.close()
		dbConn.close()


@app.route("/add_sub",methods=["POST"])
def add_s():
	dbConn = None
	cursor = None
	super_cat = request.form["super"]
	new_cat = request.form["new"]
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = f"""
		ALTER TABLE categoria_simples DISABLE TRIGGER remove_categoria_simples;
		DELETE FROM categoria_simples WHERE nome = %(super)s;
		ALTER TABLE categoria_simples ENABLE TRIGGER remove_categoria_simples;
		ALTER TABLE super_categoria DISABLE TRIGGER nova_super_categoria;
		INSERT INTO super_categoria VALUES (%(super)s) ON CONFLICT DO NOTHING;
		ALTER TABLE super_categoria ENABLE TRIGGER nova_super_categoria;

		INSERT INTO tem_outra VALUES (%(super)s,%(new)s);"""
		cursor.execute(query,{'super':(super_cat,),'new':new_cat})
		return redirect(user+"/add_sub")
	except Exception as e:	
		return str(e)  # Renders a page with the error.
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route("/del/<scat>/<cat>")
def dscat(scat,cat):
	dbConn = None
	cursor = None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = f"""
			WITH RECURSIVE subcategorias AS (
			SELECT
				categoria,
				super_categoria
			FROM
				tem_outra
			WHERE
				super_categoria = %(scat)s AND categoria=%(cat)s
			UNION
				SELECT
					e.categoria,
					e.super_categoria
				FROM
					tem_outra e
				INNER JOIN subcategorias s ON s.categoria = e.super_categoria
		) DELETE FROM tem_outra WHERE categoria IN (SELECT categoria FROM subcategorias) AND
		 super_categoria IN (SELECT super_categoria FROM subcategorias WHERE categoria = categoria);

		 ALTER TABLE super_categoria DISABLE TRIGGER remove_super_categoria;
		DELETE FROM super_categoria WHERE nome = %(scat)s;
		ALTER TABLE super_categoria ENABLE TRIGGER remove_super_categoria;
		ALTER TABLE categoria_simples DISABLE TRIGGER nova_categoria_simples;
		INSERT INTO categoria_simples VALUES (%(scat)s);
		ALTER TABLE categoria_simples ENABLE TRIGGER nova_categoria_simples;

		"""
		data = {'scat':scat,'cat':cat}
		cursor.execute(query,data)
		return redirect(user+"/add_sub")
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route("/ivm")
def list_ivm():
	dbConn = None
	cursor = None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "SELECT * FROM IVM;"
		cursor.execute(query)
		return render_template("ivm.html", ivms = cursor)
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		cursor.close()
		dbConn.close()

@app.route("/ivm/<fabricante>/<num_serie>")
def list_ereposicao(num_serie,fabricante):
	dbConn = None
	cursor = None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		cursor_sum = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "SELECT * FROM evento_reposicao WHERE num_serie=%(numserie)s AND fabricante = %(fab)s;"
		query_sum =  "SELECT cat, SUM(unidades) FROM (evento_reposicao NATURAL JOIN produto) WHERE num_serie=%(numserie)s AND fabricante = %(fab)s GROUP BY cat; "
		cursor.execute(query,{'numserie':num_serie,'fab':fabricante})
		cursor_sum.execute(query_sum,{'numserie':num_serie,'fab':fabricante})
		return render_template("erep.html", ereps = cursor, sums = cursor_sum,info = (fabricante,num_serie))
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		cursor.close()
		dbConn.close()


@app.route("/add_ret")
def add_ret():
	dbConn = None
	cursor = None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		ivms= dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "SELECT * FROM categoria"
		cursor.execute(query)
		query = "SELECT * FROM ivm"
		ivms.execute(query)
		return render_template("add_ret.html",cats=cursor,ivms=ivms)
	except Exception as e:
			return str(e)  # Renders a page with the error.
	finally:
		cursor.close()
		dbConn.close()

@app.route("/add_ret",methods=["POST"])
def add_r():
	dbConn = None
	cursor = None
	novo_nome = request.form["nome"]
	novo_tin = request.form["tin"]
	cats = request.form.getlist("cat")
	ivm = request.form["ivm"].split('-')
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = "INSERT INTO retalhista VALUES (%(tin)s,%(nome)s);"
		cursor.execute(query,{'nome':(novo_nome,),'tin':novo_tin})
		
		query = "INSERT INTO responsavel_por VALUES (%(cat)s,%(tin)s,%(ivm_serial)s,%(ivm_fab)s);"
		for cat in cats:
			cursor.execute(query,{'cat':cat,'tin':novo_tin,'ivm_serial':ivm[1],'ivm_fab':ivm[0]})

		return redirect(user+"/ret")
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route("/del_ret/<tin>")
def dret(tin):
	dbConn = None
	cursor = None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		data = (tin,)
		query_prep = f"""DELETE FROM responsavel_por WHERE tin = %(tin)s;""" 
		cursor.execute(query_prep,{'tin':data})
		query = "DELETE FROM retalhista WHERE tin =  %(tin)s;"
		cursor.execute(query,{'tin':data})
		return redirect(user+"/ret")
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		dbConn.commit()
		cursor.close()
		dbConn.close()

@app.route("/ret")
def ret():
	dbConn = None
	cursor = None
	try:
		dbConn = psycopg2.connect(DB_CONNECTION_STRING)
		cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = f"""SELECT * FROM retalhista"""
		cursor.execute(query)
		return render_template("ret.html", rets=cursor)
	except Exception as e:
		return str(e)  # Renders a page with the error.
	finally:
		cursor.close()
		dbConn.close()

CGIHandler().run(app)

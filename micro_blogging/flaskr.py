import sqlite3
from flask import Flask, request, session, redirect, g, url_for, abort, render_template, flash

database = "/tmp/microblog.db"
debug = True
secret_key = "development key"
username = "admin"
password = "defaultpass"
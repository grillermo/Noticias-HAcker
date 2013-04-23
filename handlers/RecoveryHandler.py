#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#Copyright (c) 2011 - Santiago Zavala
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import logging
import hashlib
import keys
import prefetch
import helper
import random

from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.ext.webapp.util import run_wsgi_app

from datetime import datetime, date, timedelta
from gaesessions import get_current_session
from django.utils import simplejson

from libs import PyRSS2Gen
from models import User, Post, Comment, Vote, Notification, Ticket


#register the desdetiempo filter to print time since in spanish
template.register_template_library('filters.CustomFilters')

class Handler(webapp.RequestHandler):
  def get(self,code):
    session = get_current_session()
    code = helper.parse_post_id(code)
    if session.has_key('error'):
      error = session['error']
    
    ticket = Ticket.all().filter('code',code).filter('is_active',True).fetch(1)
    if len(ticket) == 1:
      ticket = ticket[0]
      self.response.out.write(template.render('templates/new-password.html', locals()))
    else:
      self.redirect('/')

  def post(self,code):
    session = get_current_session()
    code = helper.parse_post_id(helper.sanitizeHtml(self.request.get('code')))
    password = helper.sanitizeHtml(self.request.get('password'))
    password_confirm = helper.sanitizeHtml(self.request.get('password_confirm'))
    if password != password_confirm :
      session['error'] = "Ocurrió un error al confirmar el password"
      self.redirect('/recovery/'+code)
      return
    ticket = Ticket.all().filter('code',code).filter('is_active',True).fetch(1)
    if len(ticket) == 1:
      ticket = ticket[0]
      user = ticket.user
      user.password = User.slow_hash(password)
      user.put()
      ticket.is_active = False
      ticket.put()
      session['success'] = "Se ha cambiado el password correctamente, ya puedes iniciar sesión con tus nuevas credenciales"
      self.redirect('/login')
    else:
      self.redirect('/')




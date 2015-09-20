#!/usr/bin/env python

from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys
import commands



UI = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.18.3 -->
<interface>
  <requires lib="gtk+" version="3.0"/>
  <object class="GtkWindow" id="window">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="title" translatable="yes">TOR-switch</property>
    <property name="icon_name">preferences-other</property>
    <signal name="destroy" handler="on_window_destroy" swapped="no"/>
    <child>
      <object class="GtkGrid" id="grid1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="row_spacing">2</property>
        <child>
          <object class="GtkSwitch" id="switch1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="margin_left">20</property>
            <property name="margin_right">20</property>
            <property name="margin_top">10</property>
            <property name="margin_bottom">10</property>
	    <signal name="state-set" handler="tor_cambio"/>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkSwitch" id="switch2">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="margin_left">20</property>
            <property name="margin_right">20</property>
            <property name="margin_top">10</property>
            <property name="margin_bottom">10</property>
	    <signal name="state-set" handler="proxy_cambio"/>
          </object>
          <packing>
            <property name="left_attach">0</property>
            <property name="top_attach">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="margin_left">20</property>
            <property name="margin_right">20</property>
            <property name="margin_top">10</property>
            <property name="margin_bottom">10</property>
            <property name="hexpand">True</property>
            <property name="label" translatable="yes">TOR daemon</property>
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="top_attach">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkLabel" id="label2">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="margin_left">20</property>
            <property name="margin_right">20</property>
            <property name="margin_top">10</property>
            <property name="margin_bottom">10</property>
            <property name="hexpand">True</property>
            <property name="label" translatable="yes">Socks Proxy</property>
          </object>
          <packing>
            <property name="left_attach">1</property>
            <property name="top_attach">2</property>
          </packing>
        </child>
        <child>
          <placeholder/>
        </child>
        <child>
          <placeholder/>
        </child>
      </object>
    </child>
  </object>
</interface>

"""



class GUI:
	
		
	def __init__(self):
		

		self.builder = Gtk.Builder()
		self.builder.add_from_string(UI)

		window = self.builder.get_object('window')
		tor = self.builder.get_object('switch1')
		proxy = self.builder.get_object('switch2')

		##Verificar si TOR esta corriendo y actualizar banderas
		output = commands.getoutput('ps -A')
		if ' tor' in output:
			tor.set_state(1)
		proxy_mode = commands.getoutput('dconf read /system/proxy/mode')
		proxy_port = commands.getoutput('dconf read /system/proxy/socks/port')
		proxy_host = commands.getoutput('dconf read /system/proxy/socks/host')
		if (proxy_mode == "'manual'" and proxy_port=="9050" and proxy_host=="'127.0.0.1'"):
			proxy.set_state(1)
		##/
		
		self.builder.connect_signals(self)
		window.show_all()
		window.set_resizable(0)

	
	def tor_cambio(window,self,state):
		if state == 1:
			commands.getoutput('service tor start')
			print "Activando TOR"
		if state == 0:
			commands.getoutput('service tor stop')
			print "Desactivando TOR"
		output = commands.getoutput('ps -A')
		if ' tor' in output:
			self.set_state(1)
		else:
			self.set_state(0)

	def proxy_cambio(window,self,state):
		if state == 1:
			print "Activando proxy"
			commands.getoutput("""dconf write /system/proxy/socks/host "'127.0.0.1'" """)
			commands.getoutput("dconf write /system/proxy/socks/port 9050") 
			commands.getoutput("""dconf write /system/proxy/mode "'manual'" """)
			
		if state == 0:
			print "Desactivando proxy"
			commands.getoutput("""dconf write /system/proxy/mode "'none'" """)

	def on_window_destroy(self, window):
		Gtk.main_quit()

def main():
	
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())

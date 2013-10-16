import sys
import re

class Router:
	"""
	This module provides a simple way to decide program action
	based on the command line parameters. This is particularly
	useful for scripts that will be called by the server,
	as it allows simple processing of the URI.

	The Router class is the main brain of the routing module.
	"""
	routed = False

	def __init__(self,argv = sys.argv[2:]):
		"""
		Creates a new router that will route based on the arguments provided.

		@param argv: The arguments to route on. The default argv is sys.argv
		without the first two parameters, which in server scripts corresponds
		to the HTTP method followed	by the remaining URL path.
		"""
		self.argv = argv

	def match(self,to,rule = [],options = {}):
		"""
		Attempts to match a rule. A rule consists of an array of stringss.
		These will be matched one by one respectively to the arguments provided during
		the router's initialization.
		
		Arguments can be captured into a hashtable which is sent as a parameter to the
		function provided in to.
		
			- A string will be matched verbatim but case insensitive to
			  their respective argument.
			- A string starting with ":" represents a capture, and will cause the 
			  argument to be pulled into the bindings hash. Captures can still be
			  constrained by providing a regexp that needs to be matched with the 
			  capture's name in the options.
		
		The function provided in  will be executed if the rule matches.
		
		  >>> # get playlist <id>
		  >>> r.match(lambda b: show_pl(b["playlist_id"]), ["get","playlist",":playlist_id"])
		  
		  >>> # set <numeric id>
		  >>> r.match(lambda b: set_id(int(b["id"])), ["set",":id"], { "id": "[0-9]+" })
		
		  >>> # help/info
		  >>> r.match(lambda b: show_info(), [["help","info"]])
		  
		  >>> # add <id> to <username>
		  >>> r.match(
		  ...   lambda b: add_id_to_username(int(b["id"]), b["username"]),
		  ...   ["add",":id","to",":username"],
		  ...   { "id": "[0-9]+", "username": "[a-z]+" })
		
		Generally you will want to use the helper functions provided by the
		__getattr__ implementation as it allows for a cleaner notation for standard
		queries.

		@param to: A function that will be executed when the rule matches.
		The function takes a single parameter, which is a hashtable of bound captures.

		@param rule: An array of strings that the arguments will be matched against.

		@param options: A hashtable of options. Currently this only accepts regexp
		constraints on captures.
		"""
		if len(self.argv) != len(rule):
			return

		bindings = self._match_rule(rule,self.argv,options)
		if bindings != False:
			self.routed = True
			to(bindings)

	def __getattr__(self,attr):
		"""
		Provides helper methods for the match function.
		
		When an arbitrary method is called on the Router object
		it is processed as a match where the first rule element is
		the method name as a string.
		
		This allows for a shorter and clearer notation for typical usage,
		especially when handling HTTP requests in server scripts,
		where it shows a clear difference between the HTTP method and
		the URL parts.
		
		  >>> # get playlist <id>
		  >>> r.get(lambda b: show_pl(b["playlist_id"]), ["playlist",":playlist_id"])
		  
		  >>> # set <numeric id>
		  >>> r.set(lambda b: set_id(int(b["id"])), [":id"], { "id": "[0-9]+" })
		  
		  >>> # help
		  >>> r.help(lambda b: show_help())
		  
		  >>> # add <id> to <username>
		  >>> r.add(
		  ...   lambda b: add_id_to_username(int(b["id"]), b["username"]),
		  ...   [":id","to",":username"],
		  ...   { "id": "[0-9]+", "username": "[a-z]+" })
		"""
		return lambda to,rule = [],options = {}: self._special_match(attr,to,rule,options)

	def _special_match(self,attr,to,rule = [],options = {}):
		self.match(to,[attr] + rule,options)

	def is_routed(self):
		"""
		Returns if the router has found a route for the arguments.

		@rtype: bool

		@return: True if a route has been found, False otherwise
		"""
		return self.routed

	def _match_rule_element(self,rule_el,realarg,bindings,options):
		if rule_el[0] == ":":
			rule_el = rule_el[1:]
			bindings[rule_el] = realarg
			return not rule_el in options or re.compile(options[rule_el]).match(realarg)
		elif type(rule_el) == str:
			return rule_el.lower() == realarg.lower()
		elif type(rule_el) == list:
			for el in rule_el:
				if self._match_rule_element(el,realarg,bindings,options):
					return True
			return False
		else:
			raise "Illegal rule for router match: #{rule}"

	def _match_rule(self,rule,realargs,options):
		bindings = {}
		for (rule_el,realarg) in zip(rule,realargs):
			if not self._match_rule_element(rule_el,realarg,bindings,options):
				return False
		return bindings

	def finalize(self):
		"""
		Convenience method. Throws a BaseException if no route was found.
		Call after all your match calls.
		"""
		if not self.routed:
			raise BaseException("Couldn't find a route")

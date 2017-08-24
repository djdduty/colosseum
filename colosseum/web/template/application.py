# encoding: cinje

: from collections.abc import Mapping, Iterator
: from collections import OrderedDict


: default_metadata = [
	: {'charset': "utf-8"},
	: {'http-equiv': "x-ua-compatible", 'content': "ie=edge"},
	: ("description", "content"),
	: ("viewport", "width=device-width, initial-scale=1"),
: ]


: default_scripts_before = []
: default_scripts_after = []


: def default_header title, metadata=[], styles=[], scripts=[]
		<!-- Metadata -->
	: for data in metadata
		: if isinstance(data, Mapping)
		<meta&{data}>
		: else
		<meta&{name=data[0], content=data[1]}>
		: end
	: end
		<!-- End of Metadata -->

		<title>${title}</title>

		<!-- Styles -->
	: for href in styles
		<link&{href=href, rel="stylesheet"}>
	: end

		<!-- Scripts -->
	: for href in scripts
		<script&{src=href, type="text/javascript"}></script>
	: end
: end


: def default_footer scripts=[]
		<footer></footer>

	: for script in scripts
		<script&{src=script, type="text/javascript"}></script>
	: end
: end


: def page title, header=default_header, footer=default_footer, metadata=[], styles=[], scripts=[], **attributes
	: if attributes is None
		: attributes = {}
	: end

<!DOCTYPE html>
<html&{lang=attributes.pop('lang', 'en')}>
	<head>
		: if header
			: use header title, metadata=default_metadata + metadata, styles=styles, scripts=default_scripts_before
		: end
	</head>

	<body&{attributes, role='application'}>
		: yield

		: if footer
			: use footer scripts=default_scripts_after + scripts
		: end
	</body>
</html>
: end

: def render_application assets, sub_response
	: using page title="Gigantic Colosseum", scripts=assets['colosseum_scripts'].urls(), styles=assets['colosseum_styles'].urls()
		<nav class="header">
			<li><a href="/">Official</a></li>
			<li><a href="/hero">Heroes</a></li>
			<li><a href="/lfg">lfg</a></li>
			<li><a href="/player">Players</a></li>
		</nav>
		<main class="content">
			#{sub_response}
		</main>
	: end
: end

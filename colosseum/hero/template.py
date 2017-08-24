# encoding: cinje

: from colosseum.web.template import render_application


: def render_hero_page assets, heroes
	: using render_application assets=assets
		<ul class="hero-list">
		: for hero in heroes.values()
			<li><img src='http://via.placeholder.com/250x200'><span>${hero.id}</span></li>
		: end
		</ul>
	: end
: end

# encoding: cinje

: import time

: def render_hero_page heroes, hero_translations
	<template id='hero-template'>
		<h3>Colosseum | Heroes</h3>
		<ul class="hero-list">
		: i = 0
		: for hero in heroes.values()
			: translation = hero_translations['INT'][hero.section_id]
			<li class="animated--fade"><img src='https://via.placeholder.com/250x200?random=${i}'><span>${translation.display_name} (${hero.id})</span></li>
			: i+=1
		: end
		</ul>
	</template>
: end

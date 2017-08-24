# encoding: cinje


: def render_player_page name, profile
	<template>
		<header>
			<h1>Player Profile</h1>
			<form action='/player' method='get' class='flex--right'>
				<input type='text' placeholder='Search for player...' name='name'>
			</form>
		</header>
		: if profile is not None
		<table class='player-table'>
			<tr>
				<th>Name</th>
				<th>Level</th>
				<th>Wins</th>
				<th>Losses</th>
				<th>MMR</th>
			</tr>
			<tr>
				<td>${name}</td>
				<td>${profile['all']['total']['rank']}</td>
				<td>${profile['all']['total']['wins']}</td>
				<td>${profile['all']['total']['losses']}</td>
				<td>${profile['all']['total']['motiga_skill']*100}</td>
			</tr>
		</table>
		: elif name is not None
		<h1>${name}</h1>
		: end
	</template>
: end

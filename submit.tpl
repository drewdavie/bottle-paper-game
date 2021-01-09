<html>
    <head>
        <title>Submit</title>
	    <link rel="stylesheet" href="static/ProjectStyles.css">
    </head>
    <body>

        <form action="/">
            <input type="submit" value="Home">
        </form>

        <form method="post" action="/submit_clue">
            Submit Clue: <input name='string'>
            <input type='submit' value='Submit Clue'>
        </form>
        {{message}}

        <form method="post" action="/submit_player">
            Submit Player Name: <input name='player'>
            <select name="team" id="team">
                <option value="team1">Team 1</option>
                <option value="team2">Team 2</option>
            </select>
            <input type='submit' value='Submit Player Name'>
        </form>
        {{player_message}}
    </body>
</html>
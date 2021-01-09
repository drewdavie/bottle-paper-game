<html>
  <head>
      <title>Paper Game</title>
	  <link rel="stylesheet" href="static/ProjectStyles.css">
  </head>
  <body>
    <h2>Paper Game</h2>
    <h1>Current Player: {{current_player}}</h1>
    <table>
        <tr>
            <td><h1>Clue:</h1></td><td><h1>{{string}}</h1></td>
            <td><form action="/guessed_string">
                <input type="submit" value="Guessed Clue">
            </form></td>
        </tr>
        <tr>
            <td><h1>Skipped:</h1></td><td><h1>{{skipped}}</h1></td>
            <td><form action="/guessed_skipped">
                <input type="submit" value="Guessed Skipped Clue">
            </form></td>
        </tr>
        <tr>

            <td><form action="/new_string">
                <input type="submit" value="New Clue">
            </form></td>
            <td><form action="/skip_string">
                <input type="submit" value="Skip Clue">
            </form></td>
            <td><form action="/end_turn">
                <input type="submit" value="End Turn">
            </form></td>
        </tr>
    </table>

    <h1>Guessed Clue Counter: {{counter}}</h1>
    <br>
        <table>
        <tr>
            <td>
                <form action="/submit">
                <input type="submit" value="Submit Clues">
                </form>
            </td>
            <td>
                <form action="/admin">
                <input type="submit" value="Admin">
                </form>
            </td>
        </tr>
    </table>
    {{!score_table}}
  </body>
</html>
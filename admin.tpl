<html>
  <head>
      <title>Admin</title>
	  <link rel="stylesheet" href="static/ProjectStyles.css">
  </head>
  <body>
       <h1>Home</h1>

       <form action="/">
           <input type="submit" value="Home">
       </form>

      <h1>Create DB</h1>
      <form action="/admin/create_DB">
          <input type="submit" value="Create DB">
      </form>

      <h1>Clean DB (Reset game with same clues)</h1>
      <form action="/admin/clean_DB">
          <input type="submit" value="Clean DB">
      </form>

            <h1>Delete DB (Delete all clues and players)</h1>
      <form action="/admin/delete_DB">
          <input type="submit" value="Delete DB">
      </form>
  </body>
</html>
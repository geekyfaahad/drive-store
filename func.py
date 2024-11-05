from markupsafe import Markup
def generate_header():
    h = Markup('''
    <div class="headerrr">
		<form action="/create" method="POST">
		   <button type="button" class="create" onclick="sweet()">Create Folder</button>
		 </form>
                  <a href="/" style="text-decoration:none;">
        <h1 style="font-family: Times New Roman, Times, serif; color: #000; text-decoration: none; font-size: 32px; font-weight: lighter; text-align: center; font-size: 26px; margin-top: -40px;margin-right: -8px;">
            Drive Store
        </h1>
    </a>
    <div id="yuu">
        <a href="javascript:profile();">
            <img src="../static/img/avatar.png" class="avatar" style="float: right;">
        </a>
    </div>
   </div>

    ''')

    return h

masthead=generate_header()
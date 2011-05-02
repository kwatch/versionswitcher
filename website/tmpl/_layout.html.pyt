<?py # -*- coding: utf-8 -*- ?>
<?py #@ARGS _content, self, page_title ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!--
Design by Free CSS Templates
http://www.freecsstemplates.org
Released for free under a Creative Commons Attribution 2.5 License

Name       : Indication
Description: A two-column, fixed-width design with dark color scheme.
Version    : 1.0
Released   : 20090910

Modified by kuwata-lab.com

-->
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
    <title>VersionSwitcher - ${page_title}</title>
    <meta name="keywords" content="" />
    <meta name="description" content="" />
    <link rel="stylesheet" type="text/css" href="/css/style.css" media="screen" />
    <link rel="stylesheet" type="text/css" href="/css/site.css" media="screen" />
    <?py css_files = self.context.get('css_files', ()) ?>
    <?py for fname in css_files: ?>
    <link rel="stylesheet" type="text/css" href="/css/${fname}" />
    <?py #endfor ?>
    <script language="javascript" type="text/javascript" src="/js/jquery-1.5.min.js"></script>
    <?py js_files = self.context.get('js_files', ()) ?>
    <?py for fname in js_files: ?>
    <script language="javascript" type="text/javascript" src="/js/${fname}"></script>
    <?py #endfor ?>
    <link rel="shortcut icon" href="/favicon.ico" />
  </head>
  <body>
    <div id="wrapper">


      <div id="header">
        <div id="logo">
          <h1><a href="/">VersionSwitcher</a></h1>
          <p>a small utility to switch versions of programming languages</p>
        </div>
      </div><!-- /header -->


      <div id="menu">
        <ul>
          <?py m = re.match(r'/\w+', self.request.path) ?>
          <?py current = (m.group(0) if m else '/index') ?>
          <?py d = { current: ' class="current_page_item"' } ?>
          <li #{d.get('/index')}><a href="/">Home</a></li>
          <li #{d.get('/document')}><a href="/document.html">Document</a></li>
          <li #{d.get('/history')}><a href="/history.html">History</a></li>
        </ul>
      </div><!-- /menu -->


      <div id="page">
        <div id="page-bgtop">
          <div id="page-bgbtm">


            <div id="content">
              #{_content}
              <div style="clear: both;">&nbsp;</div>
            </div><!-- /content -->


            <div id="sidebar">
              <ul>
                <?py include('_sidebar.html.pyt') ?>
              </ul>
            </div><!-- /sidebar -->


            <div style="clear: both;">&nbsp;</div>
          </div>
        </div>
      </div><!-- /page -->


    </div><!-- /wrapper -->


    <div id="footer">
      <p>Copyright $copy 2011 kuwata-lab.om. All rights reserved. Design by <a href="http://www.freecsstemplates.org/">Free CSS Templates</a>.</p>
    </div><!-- /footer -->


  </body>
</html>

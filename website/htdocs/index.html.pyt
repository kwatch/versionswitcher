<?py # -*- coding: utf-8 -*- ?>
<?py #@ARGS ?>
<?py
   _context['page_title'] = 'a small utility to switch versions of programming languages and applications'
?>

<div class="post" id="About">
  <h2 class="title"><a href="#About">About VersionSwitcher</a></h2>
  <p>Versionswitcher is a tool focused on the following features:</p>
  <ul class="simple">
    <li>Easy to intall Python, Ruby, Node.js, Perl, and so on.</li>
    <li>Easy to switch version of Python, Ruby, Node.js, Perl, and so on.</li>
  </ul>
  <p>In other words, Versionswitcher is a tool similar to RVM for any programming language.</p>
  <p>VersionSwitch requires Bash or Zsh on Unix-like system or MacOSX.</p>
  <!--p>See <a href="/document.html#Installation">document</a> for installation.</p-->
</div>


<div class="post" id="Setup">
  <h2 class="title"><a href="#Setup">Setup</a></h2>
  <pre class="terminal">
[bash]$ curl -O http://versionswitcher.appspot.com/install.sh
[bash]$ # or wget http://versionswitcher.appspot.com/install.sh
[bash]$ bash install.sh      # or zsh install.sh if you are a zsh user
[bash]$ bash                 # restart bash or zsh to enable settings
[bash]$ export VS_HOME=$HOME/vs
</pre>
</div>


<div class="post" id="Install">
  <h2 class="title"><a href="#Install">How to install Python, Ruby, Node.js, ...</a></h2>
  <pre class="terminal">
[bash]$ <strong>vs -i</strong>                # list installable languages
[bash]$ <strong>vs -i python</strong>         # list installable versions of Python
[bash]$ <strong>vs -i python 2.7.3</strong>   # start to install Python 2.7.3
[bash]$ ls -F $VS_HOME
python/
[bash]$ ls -F $VS_HOME/python
2.7.3/
</pre>
</div>


<div class="post" id="Switch">
  <h2 class="title"><a href="#Switch">How to switch version of Python, Ruby, Node.js, ...</a></h2>
  <pre class="terminal">
[bash]$ <strong>vs</strong>                   # list installed languages
[bash]$ <strong>vs python</strong>            # list installed versions of Python
[bash]$ <strong>vs python 2.7.3</strong>      # switch to 2.7.3
[bash]$ <strong>vs python 2.7</strong>        # switch to latest of 2.7.x installed
[bash]$ <strong>vs python 2</strong>          # switch to latest of 2.x.x installed
[bash]$ <strong>vs python latest</strong>     # switch to latest (ex. 3.2.2 or 2.7.3)
[bash]$ <strong>vs python -</strong>          # switch to system-installed (ex. /usr/bin/python)
</pre>
</div>


<div class="post" id="License">
  <h2 class="title"><a href="#License">License</a></h2>
  <ul>
    <li>Public Domain</li>
  </ul>
  <!--
  <table class="docinfo" frame="void" rules="none">
    <tbody valign="top">
      <tr class="field">
        <th class="docinfo-name">License:</th><td class="field-body">Public Domain</td>
      </tr>
      <tr class="field">
        <th class="docinfo-name">Copyright:</th><td class="field-body">copyright(c) 2011 kuwata-lab.com all rights reserved</td>
      </tr>
    </tbody>
  </table>
  -->
</div>

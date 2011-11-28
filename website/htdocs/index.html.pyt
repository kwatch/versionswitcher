<?py # -*- coding: utf-8 -*- ?>
<?py #@ARGS ?>
<?py
   _context['page_title'] = 'a small utility to switch versions of programming languages and applications'
?>

<div class="post" id="About-VersionSwitcher">
  <h2 class="title"><a href="#About-VersionSwitcher">About VersionSwitcher</a></h2>
  <p>VersionSwitcher is a small utility to switch version of programming language
    or application.
    <!-- Switching mechanism is just modiying $PATH environment
    variable, therefore it doesn't depend on a certain programming language
    or application.-->
    </p>
</div>


<div class="post" id="Example">
  <h2 class="title"><a href="#Example">Example</a></h2>
  <pre class="terminal">
###
### install versionswitcher
###
[bash]$ wget http://versionswitcher.appspot.com/install.sh
[bash]$ bash install.sh       # or zsh install.sh if you are a zsh user
[bash]$ bash                  # restart bash or zsh to enable settings
[bash]$ export VS_PATH=$HOME/lang
###
### install python, ruby, node, and so on
###
[bash]$ <strong>vs -i</strong>                 # list installable languages
[bash]$ <strong>vs -i python</strong>          # list installable versions
[bash]$ <strong>vs -i python 2.6.6</strong>    # install Python 2.6.6
[bash]$ <strong>vs -i python 2.7.1</strong>    # install Python 2.7.1
[bash]$ <strong>vs -i python 3.2.0</strong>    # install Python 3.2.0
[bash]$ ls -F $VS_PATH/python
2.6.6/          2.7.1/          3.2.0/
[bash]$ <strong>vs python</strong>             # list python verions installed
## basedir: /home/yourname/lang/python
## versions:
2.6.6
2.7.1
3.2.0
[bash]$ <strong>vs</strong>                    # list language names installed
python               # /home/yourname/lang/python
###
### switch version
###
[bash]$ which python          # using system-installed python
/usr/bin/python
[bash]$ <strong>vs python 2.6.6</strong>       # switch to 2.6.6
[bash]$ which python
/home/yourname/lang/python/<strong>2.6.6</strong>/bin/python
[bash]$ <strong>vs python 2.</strong>          # switch to latest version of 2.x
[bash]$ which python
/home/yourname/lang/python/<strong>2.7.1</strong>/bin/python
[bash]$ <strong>vs python latest</strong>      # switch to latest version
[bash]$ which python
/home/yourname/lang/python/<strong>3.2.0</strong>/bin/python
[bash]$ <strong>vs python -</strong>           # switch to system-installed python
[bash]$ which python
/usr/bin/python
</pre>
</div>


<div class="post" id="Features">
  <h2 class="title"><a href="#Features">Features</a></h2>
  <ul class="simple">
    <li>Switch language version by modifying $PATH environment variable.</li>
    <li>Supports any programming languages such as Ruby, Python, Node.js, and
      so on (you don't have to change switcher tool for each language).</li>
  </ul>
  <p>VersionSwitch requires Bash or Zsh on Unix-like system or Mac OS X.</p>
  <p>See <a href="/document.html#Installation">document</a> for installation.</p>
</div>


<div class="post" id="License">
  <h2 class="title"><a href="#License">License</a></h2>
  <ul>
    <li>Public Domain</li>
    <li>Copyright(c) 2011 kuwata-lab.com all rights reserved.</li>
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

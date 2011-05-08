<?py # -*- coding: utf-8 -*- ?>
<?py #@ARGS ?>
<?py
   _context['page_title'] = 'document'
?>

<div class="post" id="Usage">
  <h2 class="title"><a href="#Usage">Usage</a></h2>
  <p>Go to <a href="#Install-VersionSwitcher">Install VersionSwitcher</a> section at first if you have not installed yet.</p>
  <pre class="terminal">
[bash]$ ls -F $HOME/lang/python           # several versions are installed
2.5.5/          2.7.1/          3.1.3/
2.6.6/          3.0.1/          3.2.0/
[bash]$ wget http://versionswitcher.appspot.com/install.sh
[bash]$ bash install.sh       # or zsh install.sh if you are a zsh user
[bash]$ bash                  # restart bash or zsh to enable settings
[bash]$ VS_PATH=$HOME/lang    # setup
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
[bash]$ <strong>vs python</strong>             # list python verions installed
[bash]$ <strong>vs</strong>                    # list language names installed
</pre>
<!--
<pre class="terminal">
[bash]$ . /some/where/to/versionswitcher.sh
[bash]$ VS_PATH=$HOME/lang
[bash]$ vs python 2.6.6   # use $HOME/lang/python/2.6.6
[bash]$ vs python 2       # use $HOME/lang/python/2.x.x (ex. 2.7.1)
[bash]$ vs python latest  # use latest version under $HOME/lang/python
[bash]$ vs python -       # use system-installed one (ex. /usr/bin/python)
[bash]$ vs python         # show installed versions of python
[bash]$ vs                # show all languages installed
</pre>
-->
  <div class="tips">
    <p>Tips: Shell variables $<em>xxx</em>root and $<em>xxx</em>version are set automatically when switching.
        For example, shell variables $rubyroot and $rubyversion are set when you execute <code>vs ruby 1.9</code>.</p>
  </div>
  <div class="tips">
    <p>Tips: $HOME/.vs/hooks/&lt;language&gt;.sh is imported if exists.
        For example:</p>
<pre class="code">
## $HOME/.vs/hooks/ruby.sh
if [ -n &quot;$rubyroot&quot; ]; then
    ## set prompt to show ruby version
    PS1=&quot;ruby&#64;$rubyversion&gt; &quot;
else
    ## clear prompt
    PS1=&quot;&gt; &quot;
fi
</pre>
    </p>
  </div>
</div>


<div class="post" id="Install-VersionSwitcher">
  <h2 class="title"><a href="#Install-VersionSwitcher">Install VersionSwitcher</a></h2>
  <p>Steps:</p>
  <ol class="arabic simple">
    <li>Download '<a href="/install.sh">install.sh</a>'.</li>
    <li>Start it with bash (for bash user) or zsh (for zsh user).</li>
    <li>Log out or restart bash or zsh to enable settings.</li>
  </ol>
  <p>Example:</p>
  <pre class="terminal">
[bash]$ wget http://versionswitcher.appspot.com/install.sh
[bash]$ bash install.sh    # or zsh install.sh if you are a zsh user
...(snip)...
***
*** You have to write the following lines into your ~/.bashrc:
***
***     VS_PATH=$HOME/langs     # or other directories
***     . $HOME/.vs/bootstrap.sh
***
*** Do you want to add above lines into your ~/.bashrc? [Y/n]: y
***
*** You should log out or restart bash to enable settings.
***
*** Installation is finished successfully.
*** See http://localhost:8080/ for details.
*** Thank you.
[bash]$ bash       # start new bash process
[bash]$ vs -h      # show help
</pre>
</div>


<div class="post" id="Directory-Structure">
  <h2 class="title"><a href="#Directory-Structure">Directory Structure</a></h2>
  <p>All languages you want to switch should be installed into $HOME/lang
    (or other directory where you specified by $VS_PATH) such as:</p>
<pre class="code">
+ $HOME/
  + lang/
    + ruby/
      + 1.8.7-p334/
        + bin/
          - ruby
      + 1.9.2-p180/
        + bin/
          - ruby
    + python/
      + 2.6.6/
        + bin/
          - python
      + 2.7.1/
        + bin/
          - python
      + 3.2.0/
        + bin/
          - python
    + node/
      + 0.4.7/
        + bin/
          - node
</pre>
  <p>VersionSwitcher supports <em>ANY</em> programming languages to switch as long as they are installed according to the above structure.</p>
  <div class="tips">
    <p>Tips: You can specify several directories to $VS_PATH such as <code>VS_PATH=$HOME/lang:/opt/lang:/usr/local</code>.</p>
  </div>
  <div class="tips">
    <p>Tips: If command name is different from language name, register it into versionswitcher.sh. Try <code>grep gauche versionswitcher.sh</code> for example.</p>
  </div>
</div>


<div class="post" id="Language-Installer">
  <h2 class="title"><a href="#Language-Installer">Language Installer</a></h2>
  <p>VersionSwitcher has a feature to install the following languages easily:</p>
  <ul>
    <li>Node.js (<a href="http://nodejs.org/">http://nodejs.org/</a>)</li>
    <li>Python (<a href="http://www.python.org/">http://www.python.org/</a>)</li>
    <li>PyPy (<a href="http://pypy.org/">http://pypy.org/</a>)</li>
    <li>Ruby (<a href="http://www.ruby-lang.org/">http://www.ruby-lang.org/</a>)</li>
    <li>Rubinius (<a href="http://rubini.us/">http://rubini.us/</a>)</li>
    <li>Lua (<a href="http://www.lua.org/">http://www.lua.org/</a>)</li>
    <li>LuaJIT (<a href="http://luajit.org/">http://luajit.org/</a>)</li>
  </ul>
  <div class="tips">
    <p>Tips: You must install development tools (such as compiler, header files) and wget command <em>BEFORE</em> installing languages. For example:
      <pre class="terminal">
### Debian or Ubuntu
[bash]$ sudo apt-get update
[bash]$ sudo apt-get install wget gcc g++ make patch
[bash]$ sudo apt-get install libc6-dev zlib1g-dev libssl-dev
[bash]$ sudo apt-get install libncurses5-dev libreadline-dev libgdbm-dev
[bash]$ sudo apt-get install libyaml-dev libffi-dev  # for ruby1.9
[bash]$ sudo apt-get install pkg-config              # for node.js
### Mac OS X (install XCode and MacPorts at first!)
[bash]$ which gcc
/usr/bin/gcc
[bash]$ sudo port sync
[bash]$ sudo port install wget
[bash]$ sudo port install readline subversion        # for Python2.5
</pre>
    </p>
  </div>
  <p>The following is an exaple to install Node.js (and npm command):</p>
  <pre class="terminal">
[bash]$ <strong>vs -i</strong>                # or vs --install
## try 'vs -i LANG' where LANG is one of:
lua         # http://www.lua.org/
luajit      # http://luajit.org/
node        # http://nodejs.org/
pypy        # http://pypy.org/
python      # http://www.python.org/
rubinius    # http://rubini.us/
ruby        # http://www.ruby-lang.org/
[bash]$ <strong>vs -i node</strong>
## try 'vs -i node VERSION' where VERSION is one of:
0.4.7
0.4.6
0.4.5
0.4.4
[bash]$ <strong>vs -i node latest</strong>    # or vs -i node 0.4.7
** latest version is 0.4.7
** Install into '/home/yourname/lang/node/0.4.7'. OK? [Y/n]: <strong>y</strong>
** Configure is './configure --prefix=/home/yourname/lang/node/0.4.7'. OK? [Y/n]: <strong>y</strong>
$ wget -nc http://nodejs.org/dist/node-v0.4.7.tar.gz
$ tar xzf node-v0.4.7.tar.gz
$ cd node-v0.4.7/
$ time ./configure --prefix=/home/yourname/lang/node/0.4.7
...(snip)...
$ time JOBS=2 make
...(snip)...
$ cd ..
$ hash -r
$ which node
/home/yourname/lang/node/0.4.7/bin/node

** Install npm (Node Package Manger)? [Y/n]: <strong>y</strong>
$ wget -qO - http://npmjs.org/install.sh | sh
fetching: http://registry.npmjs.org/npm/-/npm-0.3.18.tgz
0.4.7
! [ -d .git ] || git submodule update --init
node cli.js cache clean
...(snip)...
** npm installed successfully.

** Installation is finished successfully.
**   language:  node
**   version:   0.4.7
**   directory: /home/yourname/lang/node/0.4.7

** vs node 0.4.7
$ export PATH=/home/yourname/lang/node/0.4.7/bin:/usr/local/bin:/usr/bin:/bin
$ noderoot='/home/yourname/lang/node/0.4.7'
$ nodeversion='0.4.7'
$ which node
/home/yourname/lang/node/0.4.7/bin/node
</pre>
  <p>The above steps are same for other languages such as ruby, python, lua and luajit.</p>
  <div class="tips">
    <p>Tips: VersionSwitcher installs package manager for each language:</p>
    <ul>
      <li><a href="http://npmjs.org/">npm</a> (for Node.js)</li>
      <li><a href="https://rubygems.org/pages/download">RubyGems</a> (for Ruby)</li>
      <li><a href="http://packages.python.org/distribute/">Distribute</a> (for Python)</li>
    </ul>
  </div>
  
<!--
  <h3 class="title">Ruby</h3>
  <p>The following is an example to install Ruby 1.9.2 into $HOME/lang/ruby:</p>
<pre class="terminal">
[bash]$ wget ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.2-p180.tar.bz2
[bash]$ tar xjf ruby-1.9.2-p180.tar.bz2
[bash]$ cd ruby-1.9.2-p180/
[bash]$ ./configure --prefix=$HOME/lang/ruby/1.9.2-p180
[bash]$ JOBS=2 make
[bash]$ make install
[bash]$ vs ruby 1.9.2       # or vs ruby latest
[bash]$ which ruby
/home/yourname/lang/ruby/1.9.2-p378/bin/ruby
[bash]$ which gem
/home/yourname/lang/ruby/1.9.2-p378/bin/gem
[bash]$ gem -v
1.3.7
[bash]$ gem update --system
[bash]$ gem -v
1.7.2
</pre>

  <h3 class="title">Python</h3>
  <p>The following is an example to install Python 3.2 and distribute module into $HOME/lang/python:</p>
<pre class="terminal">
[bash]$ wget http://www.python.org/ftp/python/3.2/Python-3.2.tar.bz2
[bash]$ tar xjf Python-3.2.tar.bz2
[bash]$ cd Python-3.2/
[bash]$ ./configure --prefix=$HOME/lang/python/3.2.0    # not '3.2'!
[bash]$ JOBS=2 make
[bash]$ make install
[bash]$ (cd $HOME/lang/python/3.2.0/bin; ln python3.2 python)
[bash]$ vs python 3.2       # or vs python latest
[bash]$ which python
/home/yourname/lang/python/3.2.0/bin/python
[bash]$ wget http://python-distribute.org/distribute_setup.py
[bash]$ python distribute_setup.py
[bash]$ which easy_install
/home/yourname/lang/python/3.2.0/bin/easy_install
[bash]$ easy_install --version
distribute 0.6.15
[bash]$ easy_install readline     # for Mac OS X
</pre>

  <h3 class="title">Node.js</h3>
  <p>The following is an example to install Node.js 0.4.7 into $HOME/lang/node:</p>
<pre class="terminal">
[bash]$ wget http://nodejs.org/dist/node-v0.4.7.tar.gz
[bash]$ tar xzf node-v0.4.7.tar.gz
[bash]$ cd node-v0.4.7/
[bash]$ ./configure --prefix=$HOME/lang/node/0.4.7
[bash]$ JOBS=2 make
[bash]$ make test
[bash]$ make install
[bash]$ vs node 0.4.7       # or vs node latest
[bash]$ which node
/home/yourname/lang/node/0.4.7/bin/node
[bash]$ node -v
v0.4.7
[bash]$ wget http://npmjs.org/install.sh
[bash]$ sh install.sh
[bash]$ which npm
/home/yourname/lang/node/0.4.7/bin/npm
[bash]$ npm -v
0.3.18
</pre>
-->

</div>

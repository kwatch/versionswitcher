<?py # -*- coding: utf-8 -*- ?>
<?py #@ARGS ?>
<?py
   _context['page_title'] = 'Document'
?>

<div class="post" id="install">
  <h2 class="title"><a href="#install">Install</a></h2>
  <p>Steps:</p>
  <ol class="arabic simple">
    <li>Download '<a href="https://versionswitcher.appspot.com/install.sh">install.sh</a>'.</li>
    <li>Start it with bash (for bash user) or zsh (for zsh user).</li>
    <li>Log out or restart bash or zsh to enable settings.</li>
  </ol>
  <p>Example:</p>
  <pre class="terminal">
[bash]$ curl -O http://versionswitcher.appspot.com/install.sh
[bash]$ # or wget http://versionswitcher.appspot.com/install.sh
[bash]$ bash install.sh    # or zsh install.sh if you are a zsh user
...(snip)...
***
*** You have to write the following lines into your ~/.bashrc:
***
***     export VS_HOME=$HOME/vs     # or other directory
***     . $HOME/.vs/bootstrap.sh
***
*** Do you want to add above lines into your ~/.bashrc? [Y/n]: y
***
*** You should log out or restart bash to enable settings.
***
*** Installation finished successfully.
*** See http://versionswitcher.appspot.com/ for details.
*** Thank you.
[bash]$ bash       # start new bash process
[bash]$ vs -h      # show help
</pre>
</div>


<div class="post" id="usage">
  <h2 class="title"><a href="#usage">Usage</a></h2>
  <pre class="terminal">
[bash]$ ls -F $HOME/vs/python           # several versions are installed
2.5.6/          2.7.2/          3.1.4/
2.6.7/          3.0.1/          3.2.0/
[bash]$ <strong>export VS_HOME=$HOME/lang</strong>         # setup
[bash]$ which python                      # using system-installed python
/usr/bin/python
[bash]$ <strong>vs python 2.6.7</strong>       # switch to 2.6.7
[bash]$ which python
/home/yourname/vs/python/<strong>2.6.7</strong>/bin/python
[bash]$ <strong>vs python 2.</strong>          # switch to latest version of 2.x
[bash]$ which python
/home/yourname/vs/python/<strong>2.7.2</strong>/bin/python
[bash]$ <strong>vs python latest</strong>      # switch to latest version
[bash]$ which python
/home/yourname/vs/python/<strong>3.2.0</strong>/bin/python
[bash]$ <strong>vs python -</strong>           # switch to system-installed python
[bash]$ which python
/usr/bin/python
[bash]$ <strong>vs python</strong>             # list python verions installed
[bash]$ <strong>vs</strong>                    # list language names installed
</pre>
<!--
<pre class="terminal">
[bash]$ . /some/where/to/versionswitcher.sh
[bash]$ export VS_HOME=$HOME/lang
[bash]$ vs python 2.6.7   # use $HOME/vs/python/2.6.7
[bash]$ vs python 2       # use $HOME/vs/python/2.x.x (ex. 2.7.2)
[bash]$ vs python latest  # use latest version under $HOME/vs/python
[bash]$ vs python -       # use system-installed one (ex. /usr/bin/python)
[bash]$ vs python         # show installed versions of python
[bash]$ vs                # show all languages installed
</pre>
-->
  <p>It is possible to execute command on specified version <em>without</em> switching version.</p>
  <pre class="terminal">
[bash]$ vs python 2.7.2
[bash]$ which python
/home/yourname/vs/python/<strong>2.7.2</strong>/bin/python
[bash]$ vs <strong>-x</strong> python 3.2.0                 # execute $VS_HOME/python/<strong>3.2.0</strong>/bin/<strong>python</strong>
[bash]$ vs <strong>-x</strong> python 3.2.0 file.py x y z   # execute with arguments
[bash]$ vs <strong>-X</strong> python 3.2.0 2to3            # execute $VS_HOME/python/<strong>3.2.0</strong>/bin/<strong>2to3</strong>
[bash]$ vs <strong>-X</strong> python 3.2.0 2to3 --help     # execute with arguments
[bash]$ which python
/home/yourname/vs/python/<strong>2.7.2</strong>/bin/python
</pre>
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


<div class="post" id="installer">
  <h2 class="title"><a href="#installer">Language Installer</a></h2>
  <p>VersionSwitcher has a feature to install the following languages easily:</p>
  <ul>
    <li>Node.js (<a href="http://nodejs.org/">http://nodejs.org/</a>)</li>
    <li>Go (<a href="http://golang.org/">http://golang.org/</a>)</li>
    <li>Rust (<a href="http://www.rust-lang.org/">http://www.rust-lang.org/</a>)</li>
    <li>Python (<a href="http://www.python.org/">http://www.python.org/</a>)</li>
    <li>PyPy (<a href="http://pypy.org/">http://pypy.org/</a>)</li>
    <li>Ruby (<a href="http://www.ruby-lang.org/">http://www.ruby-lang.org/</a>)</li>
    <li>Rubinius (<a href="http://rubini.us/">http://rubini.us/</a>)</li>
    <li>Lua (<a href="http://www.lua.org/">http://www.lua.org/</a>)</li>
    <li>LuaJIT (<a href="http://luajit.org/">http://luajit.org/</a>)</li>
    <li>Perl (<a href="http://www.perl.org/">http://www.perl.org/</a>)</li>
    <li>Gauche (<a href="http://practical-scheme.net/gauche/">http://practical-scheme.net/gauche/</a>)</li>
  </ul>
  <div class="tips">
    <p>Tips: You must install development tools (such as compiler, header files) and 'curl' or 'wget' command <em>BEFORE</em> installing languages. For example:
      <pre class="terminal">
### Debian or Ubuntu
[bash]$ sudo apt-get update
[bash]$ sudo apt-get install curl wget build-essential
[bash]$ sudo apt-get install libc6-dev zlib1g-dev libbz2-dev libssl-dev
[bash]$ sudo apt-get install libncurses5-dev libreadline-dev libgdbm-dev
[bash]$ sudo apt-get install libyaml-dev libffi-dev  # for ruby1.9
[bash]$ sudo apt-get install pkg-config              # for node.js
[bash]$ sudo apt-get install libsqlite3-dev          # for Python
[bash]$ sudo apt-get install readline subversion     # for Python2.5
<!--
### CentOS
[bash]$ sudo yum install -y wget gcc gcc-c++ make patch
[bash]$ sudo yum install -y zlib-devel bzip2-devel openssl-devel
[bash]$ sudo yum install -y ncurses-devel readline-devel gdbm-devel
[bash]$ sudo yum install -y sqlite-devel
--></pre>
    </p>
    <p>If you are Mac OS X user, install Xcode at first.</p>
  </div>
  <p>The following is an exaple to install Node.js (and npm command):</p>
  <pre class="terminal">
[bash]$ <strong>vs -i</strong>                # or vs --install
## try 'vs -i LANG' where LANG is one of:
gauche      # http://practical-scheme.net/gauche/
go          # http://golang.org/
lua         # http://www.lua.org/
luajit      # http://luajit.org/
node        # http://nodejs.org/
perl        # http://www.perl.org/
pypy        # http://pypy.org/
pypy3       # http://pypy.org/
python      # http://www.python.org/
rubinius    # http://rubini.us/
ruby        # http://www.ruby-lang.org/
rust        # http://www.rust-lang.org/
[bash]$ <strong>vs -i node</strong>
## checking http://nodejs.org/dist/
## try 'vs -i node VERSION' where VERSION is one of:
0.5.{1,2,3,4,5,6,7,8,9,10}
0.6.{0,1,2,3,4,5,6,7,8,9,10,11}
0.7.{0,1,2,3,4}
[bash]$ <strong>vs -i node 0.7.4</strong>
** latest version is 0.7.4
** Install into '/home/yourname/vs/node/0.7.4'. OK? [Y/n]: <strong>y</strong>
** Configure is './configure --prefix=/home/yourname/vs/node/0.7.4'. OK? [Y/n]: <strong>y</strong>
$ curl -ORL http://nodejs.org/dist/node-v0.7.4.tar.gz
$ tar xzf node-v0.7.4.tar.gz
$ cd node-v0.7.4/
$ time ./configure --prefix=/home/yourname/vs/node/0.7.4
...(snip)...
$ time JOBS=2 make
...(snip)...
$ cd ..
$ hash -r
$ which node
/home/yourname/vs/node/0.7.4/bin/node

** Install npm (Node Package Manger)? [Y/n]: <strong>y</strong>
$ curl -L - http://npmjs.org/install.sh | sh
fetching: http://registry.npmjs.org/npm/-/npm-1.0.106.tgz
0.7.4
! [ -d .git ] || git submodule update --init
node cli.js cache clean
...(snip)...
** npm installed successfully.

** Installation is finished successfully.
**   language:  node
**   version:   0.7.4
**   directory: /home/yourname/vs/node/0.7.4

** vs node 0.7.4
$ export PATH=/home/yourname/vs/node/0.7.4/bin:/usr/local/bin:/usr/bin:/bin
$ noderoot='/home/yourname/vs/node/0.7.4'
$ nodeversion='0.7.4'
$ which node
/home/yourname/vs/node/0.7.4/bin/node
</pre>
  <p>The above steps are same for other languages such as ruby, python, lua and luajit.</p>
  <div class="tips">
    <p>Tips: VersionSwitcher installs package manager for each language:</p>
    <ul>
      <li><a href="http://npmjs.org/">npm</a> (for Node.js)</li>
      <li><a href="https://rubygems.org/pages/download">RubyGems</a> (for Ruby)</li>
      <li><a href="http://packages.python.org/distribute/">Distribute</a> (for Python)</li>
      <li><a href="http://cpanmin.us/">cpanm</a> (for Perl)</li>
    </ul>
  </div>

<!--
  <h3 class="title">Ruby</h3>
  <p>The following is an example to install Ruby 1.9.3 into $HOME/vs/ruby:</p>
<pre class="terminal">
[bash]$ wget ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.3-p0.tar.bz2
[bash]$ tar xjf ruby-1.9.3-p0.tar.bz2
[bash]$ cd ruby-1.9.3-p0/
[bash]$ ./configure --prefix=$HOME/vs/ruby/1.9.3-p0
[bash]$ JOBS=2 make
[bash]$ make install
[bash]$ vs ruby 1.9.3       # or vs ruby latest
[bash]$ which ruby
/home/yourname/vs/ruby/1.9.3-p0/bin/ruby
[bash]$ which gem
/home/yourname/vs/ruby/1.9.3-p0/bin/gem
[bash]$ gem -v
1.3.7
[bash]$ gem update --system
[bash]$ gem -v
1.8.11
</pre>

  <h3 class="title">Python</h3>
  <p>The following is an example to install Python 3.2 and distribute module into $HOME/vs/python:</p>
<pre class="terminal">
[bash]$ wget http://www.python.org/ftp/python/3.2/Python-3.2.tar.bz2
[bash]$ tar xjf Python-3.2.tar.bz2
[bash]$ cd Python-3.2/
[bash]$ ./configure --prefix=$HOME/vs/python/3.2.0    # not '3.2'!
[bash]$ JOBS=2 make
[bash]$ make install
[bash]$ (cd $HOME/vs/python/3.2.0/bin; ln python3.2 python)
[bash]$ vs python 3.2       # or vs python latest
[bash]$ which python
/home/yourname/vs/python/3.2.0/bin/python
[bash]$ wget http://python-distribute.org/distribute_setup.py
[bash]$ python distribute_setup.py
[bash]$ which easy_install
/home/yourname/vs/python/3.2.0/bin/easy_install
[bash]$ easy_install --version
distribute 0.6.15
[bash]$ easy_install readline     # for Mac OS X
</pre>

  <h3 class="title">Node.js</h3>
  <p>The following is an example to install Node.js 0.7.4 into $HOME/vs/node:</p>
<pre class="terminal">
[bash]$ wget http://nodejs.org/dist/node-v0.7.4.tar.gz
[bash]$ tar xzf node-v0.7.4.tar.gz
[bash]$ cd node-v0.7.4/
[bash]$ ./configure --prefix=$HOME/vs/node/0.7.4
[bash]$ JOBS=2 make
[bash]$ make test
[bash]$ make install
[bash]$ vs node 0.7.4       # or vs node latest
[bash]$ which node
/home/yourname/vs/node/0.7.4/bin/node
[bash]$ node -v
v0.7.4
[bash]$ wget http://npmjs.org/install.sh
[bash]$ sh install.sh
[bash]$ which npm
/home/yourname/vs/node/0.7.4/bin/npm
[bash]$ npm -v
1.1.1
</pre>
-->

</div>


<div class="post" id="structure">
  <h2 class="title"><a href="#structure">Directory Structure</a></h2>
  <p>All languages you want to switch should be installed into $HOME/lang
    (or other directory where you specified by $VS_HOME) such as:</p>
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
      + 2.6.7/
        + bin/
          - python
      + 2.7.2/
        + bin/
          - python
      + 3.2.0/
        + bin/
          - python
    + node/
      + 0.6.11/
        + bin/
          - node
</pre>
  <p>VersionSwitcher supports <em>ANY</em> programming languages to switch as long as they are installed according to the above structure.</p>
  <!--
  <div class="tips">
    <p>Tips: You can specify several directories to $VS_HOME such as <code>export VS_HOME=$HOME/lang:/opt/lang:/usr/local</code>.</p>
  </div>
  -->
  <!--
  <div class="tips">
    <p>Tips: If command name is different from language name, register it into versionswitcher.sh. Try <code>grep gauche $HOME/.vs/scripts/versionswitcher.sh</code> for example.</p>
  </div>
  -->
</div>

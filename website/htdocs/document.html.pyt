<?py # -*- coding: utf-8 -*- ?>
<?py #@ARGS ?>
<?py
   _context['page_title'] = 'document'
?>

<div class="post" id="Usage">
  <h2 class="title"><a href="#Usage">Usage</a></h2>
<pre class="terminal">
$ . /some/where/to/versionswitcher.sh
$ VERSIONSWITCHER_PATH=$HOME/lang
$ vs python 2.6.6   # use $HOME/lang/python/2.6.6
$ vs python 2       # use $HOME/lang/python/2.x.x (ex. 2.7.1)
$ vs python latest  # use latest version under $HOME/lang/python
$ vs python -       # use system-installed one (ex. /usr/bin/python)
$ vs python         # show installed versions of python
$ vs                # show all languages installed
</pre>
</div>


<div class="post" id="Installation">
  <h2 class="title"><a href="#Installation">Installation</a></h2>
  <ol class="arabic simple">
    <li>Download '<a href="/versionswitcher.sh">versionswitcher.sh</a>' and import it.</li>
    <li>Set shell variable $VERSIONSWITCHER_PATH.</li>
    <li>Type 'vs -h' to show help message.</li>
  </ol>
  <p>An example to install:</p>
  <pre class="terminal">
$ wget http://versionswitcher.appspot.com/versionswitcher.sh
$ . versionswitcher.sh
$ VERSIONSWITCHER_PATH=$HOME/lang
$ vs -h         # show help
</pre>
  <p>And add settings to your ~/.bashrc or ~/.zshrc:</p>
  <pre class="terminal">
$ mkdir ~/lib
$ mv versionswitcher.sh ~/lib
$ echo '. $HOME/lib/versionswitcher.sh'   &gt;&gt; ~/.bashrc
$ echo 'VERSIONSWITCHER_PATH=$HOME/lang'  &gt;&gt; ~/.bashrc
</pre>
  <p>All languages which you want to switch should be installed into $HOME/lang
    (or other directory where you specified by $VERSIONSWITCHER_PATH) such as:</p>
<pre class="code">
+ $HOME/
  + lang/
    + ruby/
      + 1.8.6-p369/
      + 1.8.7-p334/
      + 1.9.2-p378/
    + python/
      + 2.5.5/
      + 2.6.6/
      + 2.7.1/
      + 3.2.0/
    + node/
      + 0.4.2/
      + 0.4.7/
</pre>

  <h3 class="title">Ruby</h3>
  <p>The following is an example to install Ruby 1.9.2 into $HOME/lang/ruby:</p>
<pre class="terminal">
$ wget ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-1.9.2-p180.tar.bz2
$ tar xjf ruby-1.9.2-p180.tar.bz2
$ cd ruby-1.9.2-p180/
$ ./configure --prefix=$HOME/lang/ruby/1.9.2-p180
$ JOBS=2 make
$ make install
$ vs ruby 1.9.2       # or vs ruby latest
$ which ruby
/home/yourname/lang/ruby/1.9.2-p378/bin/ruby
$ which gem
/home/yourname/lang/ruby/1.9.2-p378/bin/gem
$ gem -v
1.3.7
$ gem update --system
$ gem -v
1.7.2
</pre>

  <h3 class="title">Python</h3>
  <p>The following is an example to install Python 3.2 and distribute module into $HOME/lang/python:</p>
<pre class="terminal">
$ wget http://www.python.org/ftp/python/3.2/Python-3.2.tar.bz2
$ tar xjf Python-3.2.tar.bz2
$ cd Python-3.2/
$ ./configure --prefix=$HOME/lang/python/3.2.0    # not '3.2'!
$ JOBS=2 make
$ make install
$ (cd $HOME/lang/python/3.2.0/bin; ln python3.2 python)
$ vs python 3.2       # or vs python latest
$ which python
/home/yourname/lang/python/3.2.0/bin/python
$ wget http://python-distribute.org/distribute_setup.py
$ python distribute_setup.py
$ which easy_install
/home/yourname/lang/python/3.2.0/bin/easy_install
$ easy_install --version
distribute 0.6.15
$ easy_install readline     # for Mac OS X
</pre>

  <h3 class="title">Node.js</h3>
  <p>The following is an example to install Node.js 0.4.7 into $HOME/lang/node:</p>
<pre class="terminal">
$ wget http://nodejs.org/dist/node-v0.4.7.tar.gz
$ tar xzf node-v0.4.7.tar.gz
$ cd node-v0.4.7/
$ ./configure --prefix=$HOME/lang/node/0.4.7
$ JOBS=2 make
$ make test
$ make install
$ vs node 0.4.7       # or vs node latest
$ which node
/home/yourname/lang/node/0.4.7/bin/node
$ node -v
v0.4.7
$ wget http://npmjs.org/install.sh
$ sh install.sh
$ which npm
/home/yourname/lang/node/0.4.7/bin/npm
$ npm -v
0.3.18
</pre>

</div>


<div class="post" id="Tips">
  <h2 class="title"><a href="#Tips">Tips</a></h2>
  <ul>
    <li><p class="first">Short name 'vs' is an alias to function 'versionswitcher()'.</p>
    </li>
    <li><p class="first">It is allowed to set VERSIONSWITCHER_PATH=path1:path2:path3:...</p>
    </li>
    <li><p class="first">VersionSwitcher sets $xxxroot and $xxxversion shell variables.
        For example, if you execute 'vs ruby 1.9', $rubyroot and
        $rubyversion shell variables will be set.</p>
    </li>
    <li><p class="first">$HOME/.versionswitcher/hooks/&lt;language&gt;.sh is imported if exists.
        For example:</p>
<pre class="code">
## $HOME/.versionswitcher/hooks/ruby.sh
if [ -n &quot;$rubyroot&quot; ]; then
    ## set prompt to show ruby version
    PS1=&quot;ruby&#64;$rubyversion&gt; &quot;
else
    ## clear prompt
    PS1=&quot;&gt; &quot;
fi
</pre>
    </li>
  </ul>
</div>

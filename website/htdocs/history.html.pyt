<?py # -*- coding: utf-8 -*- ?>
<?py self.context['page_title'] = 'History' ?>


<div class="post">
  <h2 class="title"><a href="#">Release 0.7.1</a></h2>
  <p class="meta"><span class="posted">Aug 8, 2014</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>[Fix] 'vs' command now switches language version correctly.<br />
      <li>[Fix] Inform user to install required packages on Ubuntu or Debian.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.7.0</a></h2>
  <p class="meta"><span class="posted">Jul 31, 2014</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>[New] New option '-x' and '-X' to execute command on specified version.<br />
        ex::<br />
<pre class="terminal">
$ vs <strong>-x</strong> ruby 2.1.2       # execute $VS_HOME/ruby/2.1.2/bin/ruby
$ vs <strong>-x</strong> ruby 2.1.2 file.rb arg1 arg2  # execute with arguments
$ vs <strong>-X</strong> ruby 2.1.2 gem   # execute $VS_HOME/ruby/2.1.2/bin/gem
$ vs <strong>-X</strong> ruby 2.1.2 gem install foo    # execute with arguments
</pre>
</li>
      <li>[New] Go language installer supported.</li>
      <li>[New] Rust language installer supported.</li>
      <li>[Fix] Node.js installer fixed to work with 0.10 or later.</li>
      <li>[Fix] Ruby installer fixed to work with new url structure.</li>
      <li>[New] Ruby installer changed to skip RDoc document generation.</li>
      <li>[Fix] Python installer fixed to download *.tgz instead of *.tar.bz2
        because *.tar.bz2 is not provided by python.org since Python 3.3.4.</li>
      <li>[Fix] Rubinius isntaller fixed to download from new url.</li>
      <li>[New] PyPy installer fixed to support PyPy3.</li>
      <li>[Fix] Gauche installer fixed to recognize 4-digits version format.</li>
      <li>[New] creates '~/.vs/bootstrap.sh' which is a symbolic link to
        '~/.vs/scripts/bootstrap.sh'.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.6.1</a></h2>
  <p class="meta"><span class="posted">Oct 02, 2012</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Fix python installer script to support Python 3.3.0.</li>
      <li>Fix installer script error '-bash: [: : integer expression expected'.</li>
      <li>Change installer not to download language installer script.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.6.0</a></h2>
  <p class="meta"><span class="posted">Feb 20, 2012</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Change to rename environment variable '$VS_PATH' to '$VS_HOME'.</li>
      <li>Enhance '-i' option to add '*' after version number installed.</li>
      <li>Enhance to add 'misc/python.profile' which can be alternative of Python's virtualenv.</li>
      <li>Enhance 'hooks/python.sh' to consider 'misc/python.profile'.</li>
      <li>Change not to execute 'which' command when switching language version.</li>
      <li>Change '-U' (self upgrade) option to '-u'.</li>
      <li>Change '-u' (self upgrade) to confirm when overwriting existing hook scripts.</li>
      <li>Fix bugs which happened on zsh.</li>
      <li>Fix configure command of Perl installer script.</li>
      <li>Update RubyGems version installed to 1.8.17.</li>
      <li>Change Rubinius installer to check whether g++ and rake are installed.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.5.0</a></h2>
  <p class="meta"><span class="posted">Nov 29, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Enhance '-i' option to access to download page of each language in order to get installable versions.</li>
      <li>Enhance to add '-U' option for self-upgrade.</li>
      <li>Enhance to suppoert Perl installer.</li>
      <li>Enhance to suppoert Gauche installer.</li>
      <li>Change output format of '-i' option when showing versions.</li>
      <li>Change installer scripts to prefer 'curl' rather than 'wget'.</li>
      <li>Change installer scripts to invoke 'make' command with 'nice -10'.</li>
      <li>Document updated.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.4.1</a></h2>
  <p class="meta"><span class="posted">Nov 28, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Fix Ruby installer to install Rubygems correctly.</li>
      <li>Update Rubygems version installed to 1.8.11.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.4.0</a></h2>
  <p class="meta"><span class="posted">Nov 25, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Follow new download url of PyPy.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.3.3</a></h2>
  <p class="meta"><span class="posted">Nov 24, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Fix 'ruby' installer to install on Ruby 1.8.5 or older.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.3.2</a></h2>
  <p class="meta"><span class="posted">Nov 21, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Fix 'node' installer to follow change of Node download page.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.3.1</a></h2>
  <p class="meta"><span class="posted">May 18, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Fix 'ruby' installer to remove duplicated '.tar' extension.</li>
      <li>Fix 'versionswitcher.sh' to report error when download by wget is failed.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.3.0</a></h2>
  <p class="meta"><span class="posted">May 08, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Enhance to provide 'install.sh' to make installation easy.</li>
      <li>Enhance to provide 'bootstrap.sh' to import versionswitcher.sh lazily.</li>
      <li>Enhance to add PyPy and Rubinius as installable languages.</li>
      <li>Enhance to define a directory '$HOME/.vs' which stores scripts and data.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.2.0</a></h2>
  <p class="meta"><span class="posted">May 01, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Enhance to support '-i' option to install languages.</li>
      <li>Changed to sort version number correctly when detecting latest version.</li>
      <li>Document updated.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.1.1</a></h2>
  <p class="meta"><span class="posted">April 28, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Fix a typo.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->


<div class="post">
  <h2 class="title"><a href="#">Release 0.1.0</a></h2>
  <p class="meta"><span class="posted">April 27, 2011</span></p>
  <div style="clear: both;">&nbsp;</div>
  <div class="entry">
    <ul>
      <li>Public release.</li>
    </ul>
    <!--p class="links"><a href="#">Comments</a></p-->
  </div>
</div><!-- /post -->

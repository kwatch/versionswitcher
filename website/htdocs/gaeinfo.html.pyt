<?py # -*- coding: utf-8 -*- ?>
<?py #@ARGS self ?>
<?py
   _context['_sidebar'] = False
   skip_attrs = 'delattr dict getattribute hash init module new reduce reduce_ex repr setattr str weakref'.split()
   skip_attrs_dict = dict.fromkeys(["__" + k + "__" for k in skip_attrs], True)
 ?>

<div id="links"u>
  <a href="#Envrion">Environ</a> |
  <a href="#Request-Headers">Request Headers</a> |
  <a href="#Request">Request</a> |
  <a href="#Cookie">Cookie</a> |
  <a href="#Response-Headers">Response Headers</a> |
  <a href="#Response">Response</a>
</div>

<div class="post" id="Environ">
  <h2 class="title"><a href="#Environ">Environ (self.request.envrion)</a></h2>
  <table class="list">
    <?py for k in sorted(self.request.environ.keys()): ?>
    <?py     v = self.request.environ[k] ?>
    <tr class="">
      <th>${k}</th>
      <td>${repr(v)}</td>
    </tr>
    <?py #endfor ?>
  </table>
  [<a href="#links">top</a>]
</div>

<div class="post" id="Request-Headers">
  <h2 class="title"><a href="#Request-Headers">Request Headers (self.request.headers)</a></h2>
  <table class="list">
    <?py for k, v in self.request.headers.iteritems(): ?>
    <tr class="">
      <th>${k}</th>
      <td>${repr(v)}</td>
    </tr>
    <?py #endfor ?>
  </table>
  [<a href="#links">top</a>]
</div>

<div class="post" id="Request">
  <h2 class="title"><a href="#Request">Request (self.request)</a></h2>
  <table class="list">
    <?py for k in dir(self.request): ?>
    <?py     v = getattr(self.request, k) ?>
    <?py     if k not in skip_attrs_dict: ?>
    <tr class="">
      <th>${k}</th>
      <td>${repr(v)}</td>
    </tr>
    <?py     #endif ?>
    <?py #endfor ?>
  </table>
  [<a href="#links">top</a>]
</div>

<div class="post" id="Cookie">
  <h2 class="title"><a href="#Cookie">Cookie (self.request.cookies)</a></h2>
  <table class="list">
    <?py for k in sorted(self.request.cookies.keys()): ?>
    <?py     v = self.request.cookies[k] ?>
    <tr class="">
      <th>${k}</th>
      <td>${repr(v)}</td>
    </tr>
    <?py #endfor ?>
  </table>
  [<a href="#links">top</a>]
</div>

<div class="post" id="Response-Headers">
  <h2 class="title"><a href="#Response-Headers">Response Headers (self.response.headers)</a></h2>
  <table class="list">
    <?py for k, v in self.response.headers.items(): ?>
    <tr class="">
      <th>${k}</th>
      <td>${repr(v)}</td>
    </tr>
    <?py #endfor ?>
  </table>
  [<a href="#links">top</a>]
</div>

<div class="post" id="Response">
  <h2 class="title"><a href="#Response">Response (self.response)</a></h2>
  <table class="list">
    <?py classobj = self.response.__class__ ?>
    <?py for k in dir(self.response): ?>
    <?py     v = getattr(self.response, k) ?>
    <?py     if k not in skip_attrs_dict: ?>
    <tr class="">
      <th>${k}</th>
      <td>${repr(v)}</td>
    </tr>
    <?py     #endif ?>
    <?py #endfor ?>
  </table>
  [<a href="#links">top</a>]
</div>

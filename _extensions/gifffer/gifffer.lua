return {
  Meta = function(meta)
    if meta.gifffer then
      quarto.doc.add_html_dependency({
        name = 'gifffer',
        scripts = {'resources/gifffer.min.js'},
        stylesheets = {'resources/bjc-gifffer.css'},
        head = '<script type="text/javascript">window.onload = function() {Gifffer();};</script>'
      })
    end
  end
}

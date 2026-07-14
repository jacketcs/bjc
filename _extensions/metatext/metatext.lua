-- {{< metatext KEY >}} — emit the plain-text value of a metadata field.
--
-- Like {{< meta KEY >}}, but strips any inline HTML/markup so the result is
-- safe to interpolate into a plain-text context such as `pagetitle` (the HTML
-- <title> element, which cannot render tags). For example a title of
-- "Snap<em>!</em> Cheat Sheet" yields "Snap! Cheat Sheet" instead of leaking
-- the literal <em> tags into the browser tab.
--
-- pandoc.utils.stringify drops RawInline (raw HTML) nodes while keeping their
-- surrounding text, which is exactly the behavior we want.
return {
  ['metatext'] = function(args, kwargs, meta)
    local key = pandoc.utils.stringify(args[1])
    local field = meta[key]
    if field == nil then
      return pandoc.Inlines({})
    end
    return pandoc.Inlines({ pandoc.Str(pandoc.utils.stringify(field)) })
  end
}

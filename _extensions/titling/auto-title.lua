-- Not used because quarto doesn't have appropriate behavior
-- with this for the navigation bar

tt = require("titling")

return {
    Meta = function(meta)
      if tt.page() then
        meta.title:insert(1, pandoc.Str('Page'))
        meta.title:insert(2, pandoc.Space())
        meta.title:insert(3, pandoc.Str('' .. tt.page() .. ":"))
        meta.title:insert(4, pandoc.Space())
      end
      return meta
    end
}
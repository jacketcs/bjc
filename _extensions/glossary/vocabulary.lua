function Div(div)
  if div.classes:includes("vocab") or div.classes:includes("vocabBig") then
    local c = div.content
    print(c[1])
  end
end

return {Div = Div}
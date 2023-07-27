local function getCurrFile()
  return pandoc.path.filename(quarto.doc.input_file)
end

function unitlabpage()
  proj_fol = quarto.project.directory
  curr_file_path = quarto.doc.input_file
  curr_file = getCurrFile()
  result = ""
  if proj_fol then
    rel_path_list = pandoc.path.split(pandoc.path.make_relative(curr_file_path, proj_fol))
    for i = 1, #rel_path_list do
      if i == 1 then
        if rel_path_list[i]:find("unit") then
          result = result .. "Unit " .. rel_path_list[i]:match("%d")
        end
      elseif i == 2 then
        if rel_path_list[i]:find("lab") then
          result = result .. ", Lab " .. rel_path_list[i]:match("%d")
          result = result .. ", Page " .. curr_file:match("%d")
        end
      end
    end
  end
  return result
end

function pagenum()
  curr_file = getCurrFile()
  if curr_file:find("^%d") then
    return tonumber(curr_file:match("^%d+"))
  end
  return 0
end

function paged(args)
  if pagenum() then
    return 'Page ' .. pagenum() .. ": " .. pandoc.utils.stringify(args)
  end
end

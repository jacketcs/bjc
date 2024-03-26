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

function unitlab()
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
end

function paged(args)
  if pagenum() then
    return 'Page ' .. pagenum() .. ": " .. pandoc.utils.stringify(args)
  end
end

function pagetitle(args, kwargs, meta) 
  local title = 'title'
  local subtitle= 'subtitle'
  if meta['title'] then
    title = meta['title']
  end
  if meta['subtitle'] then
    subtitle = meta['subtitle']
  end
  return title .. subtitle .. '| JacketCSP'
end

-- function aksdjfalksjd(meta)
--   return meta.title .. meta.subtitle
-- end 

-- local function read_metadata_file(fname)
--   local metafile = io.open(fname, 'r')
--   local content = metafile:read("*a")
--   metafile:close()
--   local metadata = pandoc.read(content, "markdown").meta
--   return metadata
-- end

-- read_metadata_file(selector.source)


-- @meta


-- function Meta(meta)
--   print(meta)
--   print(meta.pagetitle)
--   if pagenum() then
--     meta.pagetitle = unitlab() .. ", " .. pandoc.utils.stringify(meta.title) .. " | JacketCS CSP"
--   else
--     meta.pagetitle = pandoc.utils.stringify(meta.title).. " | JacketCS CSP"
--   end
--   return meta
-- end

-- pandoc.

-- getmetatable(Pa

-- {{< meta subtitle >}}{{< meta title >}}
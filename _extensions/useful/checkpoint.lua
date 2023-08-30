function checkpoint(args, kwargs)
    local text = pandoc.utils.stringify(kwargs['text'])
    local id = pandoc.utils.stringify(kwargs['id'])
    if text == '' then
      text = 'Checkpoint: Fill out this Google Form'
    end

    local template = 
      [=[<button type='button' class='btn btn-danger' data-bs-toggle='modal' data-bs-target='#checkpoint-%s'> %s </button>
      <div class='modal fade' id='checkpoint-%s' tabindex='-1' role='dialog'>
        <div class='modal-dialog modal-fullscreen'>
          <div class='modal-content'>
              <div class='modal-header'>
                  <button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button>
              </div>
              <iframe src='https://docs.google.com/forms/d/e/%s/viewform?embedded=true' frameborder='0' marginheight='0' marginwidth='0' height='613'>Loading…</iframe>
              <div class='modal-footer'>
                  <button type='button' class='btn btn-danger' data-bs-dismiss='modal'>Close</button>
              </div>
          </div>
        </div>
      </div>]=]

    return pandoc.RawInline("html", string.format(template, id, text, id , id)) 
end
/* LLAB Loader
 * Lightweight Labs system.
 * This file is the entry point for all llab pages.
 */


const THIS_FILE = 'loader.js';
const RELEASE_DATE = '2021-12-07';

// Basic llab shape.
// TODO: We should separate this out a little more...
llab = {
    loaded: {},
    paths: {
        stage_complete_functions: [],
        scripts: [],
        css_files: []
    },
    rootURL: '',
    install_directory: '',
    CONFIG_FILE_PATH: '../llab.js' // currently unsed.
};

/*
 ***********************
 ******** CONFIG *******
 ***********************
 See ../llab.js for more explanations.
 */
llab.rootURL = "/";
llab.install_directory = "llab/";
llab.llab_path = llab.rootURL + llab.install_directory;
llab.courses_path = llab.rootURL + "course/";
llab.topics_path = llab.rootURL + "topic/";
llab.topic_launch_page = llab.llab_path + "html/topic.html";
llab.alt_topic_page = llab.rootURL + "topic/topic.html";
llab.empty_curriculum_page_path = llab.llab_path + "html/empty-curriculum-page.html";
// google analytics tokens

//CSS
// reference your custom CSS files, from within llab install directory.
// Multiple CSS files is fine, include a separate push for each
// llab.paths.css_files.push('/css/bjc.css');

/////////////////////////
///////////////////////// stage 0
// Stage 0 items can be executed with no dependences.
llab.paths.scripts[0] = [];
llab.paths.scripts[0].push("lib/jquery.min.js");
llab.paths.scripts[0].push("script/library.js");
llab.paths.scripts[0].push("script/quiz/multiplechoice.js");

llab.loaded['config'] = true;
llab.loaded['library'] = false;
llab.loaded['multiplechoice'] = false
llab.paths.stage_complete_functions[0] = function() {
    return ( typeof jQuery === 'function' &&
        llab.loaded['config'] && llab.loaded['library'] );
}


/////////////////
///////////////// stage 1
llab.paths.scripts[1] = [];
llab.paths.scripts[1].push("script/curriculum.js");
llab.paths.scripts[1].push("script/course.js");
llab.paths.scripts[1].push("script/topic.js");
// llab.paths.scripts[1].push("script/lib/sha1.js");     // for brainstorm

// Doing a very weird thing delaying this until stage 1
// try to get the above files loaded faster, they only depend on jQuery.
llab.paths.stage_complete_functions[1] = function() {
    return ( llab.loaded['multiplechoice'] );
}

////////////////////
//////////////////// stage 2
// all these scripts depend on jquery, loaded in stage 1
// all quiz item types should get loaded here
llab.paths.scripts[2] = [];
llab.paths.scripts[2].push("script/quiz.js");

llab.paths.stage_complete_functions[2] = function() {
    return true; // && llab.loaded['user'];
}


//////////////

llab.getPathToThisScript = function() {
    var scripts = document.scripts;
    for (var i = 0; i < scripts.length; i += 1) {
        var src = scripts[i].src;
        if (src.endsWith('/' + THIS_FILE)) {
            return src;
        }
    }
    return '';
};

llab.thisPath = llab.getPathToThisScript();

function getTag(name, src, type) {
    var tag = document.createElement(name);

    if (src.indexOf("//") === -1) {
        src = llab.thisPath.replace(THIS_FILE, src);
    }

    var link  = name === 'link' ? 'href' : 'src';
    tag[link] = `${src}?${RELEASE_DATE}`;
    tag.type  = type;

    return tag;
}



llab.initialSetUp = function() {
    function loadScriptsAndLinks(stage_num) {
        var tag;

        // load css files
        while (llab.paths.css_files.length != 0) {
            tag = getTag("link", llab.paths.css_files.shift(), "text/css");
            tag.rel = "stylesheet";
            document.head.appendChild(tag);
        }

        // load scripts
        llab.paths.scripts[stage_num].forEach(function(scriptfile) {
            tag = getTag("script", scriptfile, "text/javascript");
            document.head.appendChild(tag);
        });

        if ((stage_num + 1) < llab.paths.scripts.length) {
            proceedWhenComplete(stage_num);
        }
    }

    function proceedWhenComplete(stage_num) {
        if (llab.paths.stage_complete_functions[stage_num]()) {
            if ((stage_num + 1) < llab.paths.scripts.length) {
                loadScriptsAndLinks(stage_num + 1);
            }
        } else {
            setTimeout(function() {
                proceedWhenComplete(stage_num);
            }, 2);
        }
    }

    // start the process
    loadScriptsAndLinks(0);

};

/////////////////////

llab.initialSetUp();

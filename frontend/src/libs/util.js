let util = {

};
util.title = function (title) {
    title = title ? title + ' - Home' : 'Memory Monitor';
    window.document.title = title;
};

export default util;
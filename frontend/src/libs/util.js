let util = {

};
util.title = function (title) {
    title = title ? title + ' - Home' : 'Disk Monitor';
    window.document.title = title;
};

export default util;

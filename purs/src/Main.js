exports.setInnerHTML = function (value) {
  return function (element) {
    return function () {
      element.innerHTML = value;
      return {};
    };
  };
};

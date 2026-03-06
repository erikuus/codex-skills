let PreserveScroll = {
  storageKey() {
    const menuKey = this.el.firstElementChild?.id || this.el.id || "anonymous";
    return `preserve-scroll:${menuKey}`;
  },

  mounted() {
    const savedScrollTop = localStorage.getItem(this.storageKey());

    if (savedScrollTop) {
      this.el.scrollTop = parseInt(savedScrollTop, 10);
    }

    this.listener = () => {
      localStorage.setItem(this.storageKey(), this.el.scrollTop.toString());
    };

    this.el.addEventListener("scroll", this.listener);
  },

  destroyed() {
    this.el.removeEventListener("scroll", this.listener);
  }
};

export default PreserveScroll;

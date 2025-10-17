class Button {
    constructor(text, onClick) {
        this.text = text;
        this.onClick = onClick;
    }
    
    render() {
        return `<button class="btn" onclick="${this.onClick}">${this.text}</button>`;
    }
}

class Modal {
    constructor(title, content) {
        this.title = title;
        this.content = content;
        this.isOpen = false;
    }
    
    open() {
        this.isOpen = true;
        console.log(`Modal "${this.title}" opened`);
    }
    
    close() {
        this.isOpen = false;
        console.log(`Modal "${this.title}" closed`);
    }
}


export { Button, Modal };

class MobileNavigation {
    constructor() {
        this.menuItems = [];
        this.isExpanded = false;
    }
    
    addMenuItem(text, link) {
        this.menuItems.push({ text, link });
    }
    
    toggleMenu() {
        this.isExpanded = !this.isExpanded;
        console.log('Mobile menu toggled:', this.isExpanded);
    }
    
    render() {
        return `
            <nav class="mobile-nav">
                <button class="menu-toggle" onclick="mobileNav.toggleMenu()">☰</button>
                ${this.isExpanded ? this.menuItems.map(item => 
                    `<a href="${item.link}">${item.text}</a>`
                ).join('') : ''}
            </nav>
        `;
    }
}

const mobileNav = new MobileNavigation();

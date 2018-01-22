function BindEvents() {
    const grid = document.querySelector('.hero-list');
    const gridRect = grid.getBoundingClientRect();
    let setDelay = (item) => {
        const itemRect = item.getBoundingClientRect();
        
        const left = itemRect.left - gridRect.left;
        const top = itemRect.top - gridRect.top;
        const dist = Math.sqrt(left * left + top * top);
        const delay = dist * 0.75;
        item.style.transitionDelay = `${delay}ms`;
    }

    document.querySelectorAll('.hero-list li').forEach((ele, i) => {
        setDelay(ele);
        ele.addEventListener('click', (e) => {
            document.querySelector('.wrap').classList.toggle('active');
        });
    });
    
    let showHeroes = () => {
        document.querySelectorAll('.hero-list li').forEach((ele, i) => {
            ele.classList.add('visible');
        });
        
        grid.classList.remove('loading');
    };
    
    showHeroes();
}

// Listen to event for importing for the hero page template
function bindController() {
    document.body.addEventListener('template.hero-template', BindEvents);
}

export default {
    bind: bindController,
};

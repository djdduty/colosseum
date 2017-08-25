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
    
    const open_cover = (ele) => {
        const cover = document.querySelector('.wrap')
        const coverBg = document.querySelector('.wrap .wrap-bg');
        
        const itemRect = ele.getBoundingClientRect();
        const coverRect = cover.getBoundingClientRect();
        let left = itemRect.left - coverRect.left;
        let top = itemRect.top - coverRect.top;
        coverBg.style.left = `${left+50}px`;
        coverBg.style.top = `${top+50}px`;
        coverBg.style.width = '100px';
        coverBg.style.height = '100px';
        coverBg.style.display = 'block';
        cover.classList.add('active');
        setTimeout(() => {
            let scaleX = cover.offsetWidth / 30;
            let scaleY = cover.offsetHeight / 30;
            coverBg.style.transform = `scale(${scaleX}, ${scaleY})`;
        }, 1);
    }
    
    const close_cover = () => {
        const cover = document.querySelector('.wrap')
        const coverBg = document.querySelector('.wrap .wrap-bg');
        coverBg.style.display = '';
        cover.classList.remove('active');
        setTimeout(() => {
            coverBg.style.transform = 'none';
            coverBg.style.width = '200px';
            coverBg.style.height = '200px';
        }, 1);
    }
    
    let cover_open = false;
    document.querySelectorAll('.hero-list li').forEach((ele, i) => {
        setDelay(ele);
        ele.addEventListener('click', (e) => {
            if(cover_open) {
                close_cover();
                cover_open = false;
            } else {
                open_cover(ele);
                cover_open = true;
            }
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

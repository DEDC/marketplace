var sidenav = document.querySelectorAll('.sidenav');
var sv_instances = M.Sidenav.init(sidenav);
var collapsible = document.querySelectorAll('.collapsible');
var col_instances = M.Collapsible.init(collapsible);
var dropdown = document.querySelectorAll('.dropdown-trigger');
var drp_instances = M.Dropdown.init(dropdown);
var select = document.querySelectorAll('select');
var select_instances = M.FormSelect.init(select);
var collapsible = document.querySelectorAll('.collapsible');
var instances_collapsible = M.Collapsible.init(collapsible);
var not_collapse = document.querySelectorAll('.not-collapse')
not_collapse.forEach(e => {
    e.addEventListener('click', function (ev) {
        ev.stopPropagation();
    })
});
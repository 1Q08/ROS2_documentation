import os
from xml.etree.ElementTree import Element, SubElement, ElementTree
from conf import distro_full_names, html_baseurl


def make_sitemapindex(sitemap_file, outputdir='build/html'):

    sitemapindex = Element('sitemapindex')
    sitemapindex.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    for distro in distro_full_names.keys():
        # 只列出实际构建出的版本目录，避免为不存在的分支生成无效条目
        if os.path.isdir(os.path.join(outputdir, distro)):
            node = SubElement(sitemapindex, 'sitemap')
            SubElement(node, 'loc').text = f'{html_baseurl}/{distro}/sitemap.xml'

    ElementTree(sitemapindex).write(sitemap_file, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    sitemap_file = 'build/html/sitemap.xml'
    make_sitemapindex(sitemap_file)

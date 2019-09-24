INSERT INTO tool (tool_id, description, name, script_name, created_on) VALUES ('11234221128', 'Data for the ISSI tutorial', 'issi_data', 'issi_tutorial.py', '2019-08-23 16:01:33.935043+00'), ('11234221124', 'Line Count Tool', 'line count', 'line_count.py', '2019-08-08 14:52:58.465063+00'), ('11234221125', 'query to xnet', 'query2_xnet', '__init__.py', '2019-08-22 17:01:33.031239+00'), ('11234221126', 'xnet to communities wordcloud', 'xnet2_communities_wordcloud', '__init__.py', '2019-08-23 14:38:14.378644+00'), ('11234221129', 'converts a xnet to a figure', 'xnet2_figure', '__init__.py', '2019-08-27 15:02:30.274831+00'), ('11234221127', 'xnet to wordcloud', 'xnet2_wordcloud', '__init__.py', '2019-08-23 14:38:51.844189+00');

INSERT INTO package (package_id, tool_id, archive_id, type, description, name, created_on) VALUES ('234221133', '11234221125', '11234221134', 'CADRE_DEFINED', 'query2_xnet_package', 'query2_xnet_package', '2019-08-22 17:32:30.308364+00'), ('234221133', '11234221125', '11234221135', 'CADRE_DEFINED', 'query2_xnet_package', 'query2_xnet_package', '2019-08-22 17:32:56.63157+00'), ('234221135', '11234221127', '11234221136', 'CADRE_DEFINED', 'xnet2_wordcloud_package', 'xnet2_wordcloud_package', '2019-08-23 14:51:55.843159+00'), ('234221136', '11234221128', '11234221137', 'CADRE_DEFINED', 'package for delivering the data for the tutorial', 'issi_data_package', '2019-08-23 17:17:34.196818+00'), ('234221137', '11234221129', '11234221136', 'CADRE_DEFINED', 'package for changing the xnet file to a figure, xnet2_figure_package', '2019-08-27 14:58:18.566756+0'), ('234221132', '11234221124', '11234221133', 'CADRE_DEFINED', 'count the number of lines in the query results', 'line_count', '2019-08-08 15:13:11.147604+00'), ('234221132', '11234221124', '11234221132', 'CADRE_DEFINED', 'count the number of lines in the query results', 'line_count', '2019-08-09 02:49:40.733112+00'), ('234221134', '11234221126', '11234221136', 'CADRE_DEFINED', 'generate wordcloud for all the different xnet communities', 'xnet2_communities_wordcloud', '2019-08-23 14:50:59.1971+00');

INSERT INTO archive (archive_id, s3_location, description, name, created_on) VALUES ('11234221132', '/cadre-file-archive/cpelikan', 'exp1 result file', 'c07d4688-bdbc-4f21-9322-d2e4c45bc253.csv', '2019-08-08 15:07:18.48721+00'), ('11234221133', '/cadre-file-archive/cpelikan', 'exp result file 2', 'fc7abc95-0553-4fcf-9997-0e86d0ededa4.csv', '2019-08-09 02:33:41.103566+00'), ('11234221134', '/cadre-file-archive/filsilva', 'edge file', 'b30d1769-9180-4533-8896-ead7d509cdeb_edges.csv', '2019-08-22 17:11:38.415709+00'), ('11234221135', '/cadre-file-archive/filsilva', 'degree 0 file', 'b30d1769-9180-4533-8896-ead7d509cdeb.csv', '2019-08-22 17:14:19.812668+00'), ('11234221136', '/cadre-file-archive/filsilva', 'xnet file', 'result.xnet', '2019-08-23 15:53:31.246952+00'), ('11234221137', '/cadre-file-archive/yan30', 'tar file', 'ISSIDemoData.tar.gz', '2019-08-23 16:26:32.048808+00');













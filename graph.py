import node
import folium

class Graph:
    def __init__(self):
        self.road_node = dict()
        self.road_edge = dict()
        self.land_node = dict()
        self.land_edge = dict()
        
##########################################################################################################################
# 차도 수준 데이터 처리
##########################################################################################################################
    def add_road_node(self, node_id, lon, lat):
        if self.get_road_node(node_id) != None:
            print('add node error : ' + node_id + "는 이미 존재하는 Node입니다.")
            return
        
        newNode = node.RoadNode(node_id, lon, lat)
        self.road_node[node_id] = newNode
        self.road_edge[newNode] = [[], []]
   
    def get_road_node(self, node_id):
        return self.road_node.get(node_id)
    
    def add_road_edge(self, go_node_id, end_node_id):
        go_node = self.get_road_node(go_node_id)
        end_node = self.get_road_node(end_node_id)
        
        if go_node == None or end_node == None:
            print('add edge error : ' + go_node_id + ' ' + end_node_id + '존재하지 않는 Node입니다.')
            return
                        
        self.road_edge[go_node][0].append(end_node)
        self.road_edge[end_node][1].append(go_node)
        
    def remove_road_node(self, node_id):
        pass
       
    def remove_road_edge(self, go_node_id, end_node_id):
        if go_node_id.isascii:
            go_node = self.get_road_node(go_node_id)
            end_node = self.get_road_node(end_node_id)
        else:
            go_node = go_node_id
            end_node = end_node_id
        
        go_list = self.road_edge[go_node][0]
        end_list = self.road_edge[end_node][1]
        
        try:
            go_list.remove(end_node)
            end_list.remove(go_node)
        except ValueError:
            print('remove edge error : ' + go_node.id + ' ' + end_node.id + '연결되어있지 않습니다.')
            return
        
        for go_land_node in go_node.land_node_list:
            for end_lnad_node in end_node.land_node_list:
                go_list = self.land_edge[go_land_node][0]
                end_list = self.land_edge[end_lnad_node][1]
                
                try:
                    go_list.remove(end_node)
                    end_list.remove(go_node)
                except ValueError:
                    continue
        
    def modify_road_node(self, node_id):
        pass
    
##########################################################################################################################
# 차로 수준 데이터 처리
##########################################################################################################################
    def add_land_node(self, node_id, road_node_id):
        road_node = self.get_road_node(road_node_id)
        
        if self.get_land_node(node_id) != None:
            print('add node error : ' + node_id + "는 이미 존재하는 Node입니다.")
            return
        if road_node == None:
            print('add node error : ' + road_node_id + "는 존재하지 않는 Node입니다.")
            return
        
        newNode = node.LandNode(node_id, road_node)
        self.land_node[node_id] = newNode
        self.land_edge[newNode] = [[], []]
        # 도로 Node에 차도 Node를 add함
        road_node.add_land(newNode)
        
    def get_land_node(self, node_id):
        return self.land_node.get(node_id)
    
    def add_land_edge(self, go_node_id, end_node_id):
        go_node = self.get_land_node(go_node_id)
        end_node = self.get_land_node(end_node_id)
        
        if go_node == None or end_node == None:
            print('add edge error : ' + go_node_id + ' ' + end_node_id + '존재하지 않는 Node입니다.')
            return
        
        self.land_edge[go_node][0].append(end_node)
        self.land_edge[end_node][1].append(go_node)
        
    def remove_land_node(self, node_id):
        pass
        # -> send
        
        
        # <- receive
        
    def remove_land_edge(self, go_node_id, end_node_id):
        go_node = self.get_land_node(go_node_id)
        end_node = self.get_land_node(end_node_id)
        
        if go_node == None or end_node == None:
            print('remove edge error : ' + go_node_id + ' ' + end_node_id + '존재하지 않는 Node입니다.')
            return
        
        go_list = self.land_edge[go_node][0]
        end_list = self.land_edge[end_node][1]
        
        try:
            go_list.remove(end_node)
            end_list.remove(go_node)
        except ValueError:
            print('remove edge error : ' + go_node_id + ' ' + end_node_id + '연결되어있지 않습니다.')
            return
        
        # 차도 수준의 edge가 사라졌을때, 차로 수준의 연결상태를 확인함
        link_check = False
        
        go_road_node = go_node.road_node
        end_road_node = end_node.road_node
        
        for land_node in go_road_node.land_node_list:
            for link_item in self.land_edge[land_node][0]:
                if link_item.road_node == end_road_node:
                    link_check = True
                    break
            # end for
            if link_check == True:
                break
        # end for
        
        if link_check == False:
            self.remove_road_edge(go_road_node, end_road_node)
        
    def modify_land_node(self, node_id):
        pass
    
##########################################################################################################################
# 데이터 시각화
##########################################################################################################################
    def print_directions(self, start_id, end_id, make_html_option = None ,detail_option = None):
        start_node = self.get_road_node(start_id)
        end_node = self.get_road_node(end_id)
        
        if start_node == None or end_node == None:
            print(start_id + ', ' + end_id + '존재하지 않는 Node입니다.')
            return
        
        queue = [(start_node, [start_node])]
        result = []
        
        while queue:
            n, path = queue.pop(0)
            if n == end_node:
                result.append(path)
            else:
                for m in set(self.road_edge[n][0]) - set(path):
                    queue.append((m, path + [m]))
        
        if len(result) == 0:
            print(start_id + '에서 ' + end_id + '으로의 경로는 존재하지 않습니다.')
            return
        
        print('BIG DIR : ', end = '')
        for root in result[0]:
            print(root.id, end = ' ')
        print()
        
        if make_html_option != None:
            self.make_html(result[0])
        
        if detail_option != None:
            self.detail_directions(result[0])



    def make_html(self, directions):
        points = []
        start_id = directions[0].id
        end_id = directions[ len(directions) - 1 ].id
        
        for root in directions:
            points.append( tuple( [float(root.lat), float(root.lon)] ) )
            endId = root.id
        
        root_map = folium.Map(location=[directions[0].lat, directions[0].lon], zoom_start=17)

        #add a markers
        for each in points:  
            folium.Marker(each).add_to(root_map)

        #fadd lines
        folium.PolyLine(points, color="red", weight=1.5, opacity=1).add_to(root_map)
        file_name = start_id + ' to ' + end_id + '.html'
        root_map.save('./rootMap/' + file_name)



    def detail_dir(self, start_id, end_id):
        start_node = self.get_road_node(start_id)
        end_node = self.get_road_node(end_id)
        
        if start_node == None or end_node == None:
            print(start_id + ', ' + end_id + '존재하지 않는 Node입니다.')
            return
        
        queue = [(start_node, [start_node])]
        result = []
        
        while queue:
            n, path = queue.pop(0)
            if n == end_node:
                result.append(path)
            else:
                for m in set(self.road_edge[n][0]) - set(path):
                    queue.append((m, path + [m]))
        
        if len(result) == 0:
            print(go_id + '에서 ' + end_id + '으로의 경로는 존재하지 않습니다.')
            return

    def detail_directions(self, directions):
        dir_len = len(directions)
        
        search_count = 0
        
        node_list = directions[search_count].land_node_list
        search_count = search_count + 1
        
        visit = []
        stack = []
        path = []
        
        for start_node in node_list:
            stack.append(start_node)
            last = None
            
            while stack and  dir_len > search_count:
                node = stack.pop()
                visit.append(node)
                link_list = self.land_edge[node][0]
                
                find_check = False
                chage_lane = None
                
                for link_node in link_list:
                    if link_node in visit:
                        continue
                    
                    if link_node.road_node == directions[search_count]:
                        path.append(node)
                        stack.append(link_node)
                        find_check = True
                        last = link_node
                        search_count = search_count + 1
                        break                    
                    
                    if link_node.road_node == node.road_node:
                        chage_lane = link_node
                # end for
                
                # 다음 차도 수준의 경로 탐색 실패시 해당 차도의 다른 차로로의 이동가능 여부를 판단
                if find_check == False and chage_lane != None:
                    path.append(node)
                    stack.append(chage_lane)
                    find_check = True
                
                if len(stack) == 0 and len(path) == 0:
                    break
                
                if find_check == False:
                    stack.append( path.pop() )
                    search_count = search_count - 1
            # end while
            
            if dir_len <= search_count and last != None:
                path.append(last)
        # end for
        
        print('SMA DIR : ', end = ' ')
        
        if len(path) == 0:
            print('세부 경로탐색 실패')
        
        for root in path:
            print(root.id, end = ' ')
        print()
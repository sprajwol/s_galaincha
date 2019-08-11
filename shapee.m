function otherArea = shapee(az, outurl, new_file)
    image = strcat(az, outurl, new_file)
    aaa = "final_"
    outf = strcat(az, outurl, aaa, new_file)
    WB = imread(image);
    BW = imcomplement(WB);
    [B,L,N,A] = bwboundaries(BW);
    imshow(BW); hold on;
    colors=['b' 'g' 'r' 'c' 'm' 'y'];
    
    
    for k=1:length(B),
        boundary = B{k};
        cidx = mod(k,length(colors))+1;
        plot(boundary(:,2), boundary(:,1),...
            colors(cidx),'LineWidth',2);

        %randomize text position for better visibility
        rndRow = ceil(length(boundary)/(mod(rand*k,7)+1));
        col = boundary(rndRow,2); row = boundary(rndRow,1);
        h = text(col+1, row-1, num2str(L(row,col)));
        set(h,'Color',colors(cidx),'FontSize',10,'FontWeight','bold');

        props = regionprops(B{k});
        otherArea = sum([props.Area]);
        fprintf('Area of shape %i = %i.\n', k,otherArea)
    end
    F = getframe;
    imwrite(F.cdata, outf, 'png');
end
